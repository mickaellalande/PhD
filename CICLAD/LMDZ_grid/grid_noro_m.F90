!
! $Id$
!
MODULE grid_noro_m
!
!*******************************************************************************

  USE print_control_mod, ONLY: lunout
  USE assert_eq_m,       ONLY: assert_eq
  PRIVATE
  PUBLIC :: grid_noro, grid_noro0, read_noro


CONTAINS


!-------------------------------------------------------------------------------
!
SUBROUTINE grid_noro(xd,yd,zd,x,y,zphi,zmea,zstd,zsig,zgam,zthe,zpic,zval,mask)
!
!-------------------------------------------------------------------------------
! Author: F. Lott (see also Z.X. Li, A. Harzallah et L. Fairhead)
!-------------------------------------------------------------------------------
! Purpose: Compute the Parameters of the SSO scheme as described in LOTT &MILLER
!         (1997) and LOTT(1999).
!-------------------------------------------------------------------------------
! Comments:
!  * Target points are on a rectangular grid:
!      iim+1 latitudes including North and South Poles;
!      jjm+1 longitudes, with periodicity jjm+1=1.
!  * At the poles, the fields value is repeated jjm+1 time.
!  * The parameters a,b,c,d represent the limits of the target gridpoint region.
!    The means over this region are calculated from USN data, ponderated by a
!    weight proportional to the surface occupated by the data inside the model
!    gridpoint area. In most circumstances, this weight is the ratio between the
!    surfaces of the USN gridpoint area and the model gridpoint area. 
!
!           (c)
!        ----d-----
!        | . . . .|
!        |        |
!     (b)a . * . .b(a)
!        |        |
!        | . . . .|
!        ----c-----
!           (d)
!  * Hard-coded US Navy dataset dimensions (imdp=2160 ; jmdp=1080) have been
!    removed (ALLOCATABLE used).
!  * iext (currently 10% of imdp) represents the margin to ensure output cells
!    on the edge are contained in input cells.
!===============================================================================
  IMPLICIT NONE
!-------------------------------------------------------------------------------
! Arguments:
  REAL, INTENT(IN)  :: xd(:), yd(:)  !--- INPUT  COORDINATES     (imdp) (jmdp)
  REAL, INTENT(IN)  :: zd(:,:)       !--- INPUT  FIELD           (imdp,jmdp)
  REAL, INTENT(IN)  :: x(:), y(:)    !--- OUTPUT COORDINATES     (imar+1) (jmar)
  REAL, INTENT(OUT) :: zphi(:,:)     !--- GEOPOTENTIAL           (imar+1,jmar)
  REAL, INTENT(OUT) :: zmea(:,:)     !--- MEAN OROGRAPHY         (imar+1,jmar)
  REAL, INTENT(OUT) :: zstd(:,:)     !--- STANDARD DEVIATION     (imar+1,jmar)
  REAL, INTENT(OUT) :: zsig(:,:)     !--- SLOPE                  (imar+1,jmar)
  REAL, INTENT(OUT) :: zgam(:,:)     !--- ANISOTROPY             (imar+1,jmar)
  REAL, INTENT(OUT) :: zthe(:,:)     !--- SMALL AXIS ORIENTATION (imar+1,jmar)
  REAL, INTENT(OUT) :: zpic(:,:)     !--- MAXIMUM ALTITITUDE     (imar+1,jmar)
  REAL, INTENT(OUT) :: zval(:,:)     !--- MINIMUM ALTITITUDE     (imar+1,jmar)
  REAL, INTENT(OUT) :: mask(:,:)     !--- MASK                   (imar+1,jmar)
!-------------------------------------------------------------------------------
! Local variables:
  CHARACTER(LEN=256) :: modname="grid_noro"
  REAL, ALLOCATABLE :: xusn(:), yusn(:)           ! dim (imdp+2*iext) (jmdp+2)
  REAL, ALLOCATABLE :: zusn(:,:)                  ! dim (imdp+2*iext,jmdp+2)
! CORRELATIONS OF OROGRAPHY GRADIENT              ! dim (imar+1,jmar)
  REAL, ALLOCATABLE :: ztz(:,:), zxtzx(:,:), zytzy(:,:), zxtzy(:,:), weight(:,:)
! CORRELATIONS OF USN OROGRAPHY GRADIENTS         ! dim (imar+2*iext,jmdp+2)
  REAL, ALLOCATABLE :: zxtzxusn(:,:), zytzyusn(:,:), zxtzyusn(:,:)
  REAL, ALLOCATABLE :: num_tot(:,:), num_lan(:,:) ! dim (imar+1,jmar)
  REAL, ALLOCATABLE :: a(:), b(:)                 ! dim (imar+1)
  REAL, ALLOCATABLE :: c(:), d(:)                 ! dim (jmar)
  LOGICAL :: masque_lu
  INTEGER :: i, ii, imdp, imar, iext
  INTEGER :: j, jj, jmdp, jmar, nn
  REAL    :: xpi, zdeltax, zlenx, weighx, xincr,  zweinor, xk, xl, xm
  REAL    :: rad, zdeltay, zleny, weighy, masque, zweisud, xp, xq, xw



!-------------------------------------------------------------------------------
  imdp=assert_eq(SIZE(xd),SIZE(zd,1),TRIM(modname)//" imdp")
  jmdp=assert_eq(SIZE(yd),SIZE(zd,2),TRIM(modname)//" jmdp")
  imar=assert_eq([SIZE(x),SIZE(zphi,1),SIZE(zmea,1),SIZE(zstd,1),SIZE(zsig,1), &
                          SIZE(zgam,1),SIZE(zthe,1),SIZE(zpic,1),SIZE(zval,1), &
                          SIZE(mask,1)],TRIM(modname)//" imar")-1
  jmar=assert_eq([SIZE(y),SIZE(zphi,2),SIZE(zmea,2),SIZE(zstd,2),SIZE(zsig,2), &
                          SIZE(zgam,2),SIZE(zthe,2),SIZE(zpic,2),SIZE(zval,2), &
                          SIZE(mask,2)],TRIM(modname)//" jmar")
!  IF(imar/=iim)   CALL abort_physic(TRIM(modname),'imar/=iim'  ,1)
!  IF(jmar/=jjm+1) CALL abort_physic(TRIM(modname),'jmar/=jjm+1',1)
  iext=imdp/10                                !--- OK up to 36 degrees cell
  xpi = ACOS(-1.)
  rad = 6371229.
  zdeltay=2.*xpi/REAL(jmdp)*rad
  WRITE(lunout,*)"*** Orography parameters at sub-cell scale ***"

!--- ARE WE USING A READ MASK ?
  masque_lu=ANY(mask/=-99999.); IF(.NOT.masque_lu) mask=0.0
  WRITE(lunout,*)'Masque lu: ',masque_lu

!--- EXTENSION OF THE INPUT DATABASE TO PROCEED COMPUTATIONS AT BOUNDARIES:
  ALLOCATE(xusn(imdp+2*iext))
  xusn(1     +iext:imdp  +iext)=xd(:)
  xusn(1          :       iext)=xd(1+imdp-iext:imdp)-2.*xpi
  xusn(1+imdp+iext:imdp+2*iext)=xd(1          :iext)+2.*xpi

  ALLOCATE(yusn(jmdp+2))
  yusn(1       )=yd(1)   +(yd(1)   -yd(2))
  yusn(2:jmdp+1)=yd(:)
  yusn(  jmdp+2)=yd(jmdp)+(yd(jmdp)-yd(jmdp-1))

  ALLOCATE(zusn(imdp+2*iext,jmdp+2))
  zusn(1       +iext:imdp  +iext,2:jmdp+1)=zd  (:                   ,     :)
  zusn(1            :       iext,2:jmdp+1)=zd  (imdp-iext+1:imdp    ,     :)
  zusn(1+imdp  +iext:imdp+2*iext,2:jmdp+1)=zd  (1:iext              ,     :)
  zusn(1            :imdp/2+iext,       1)=zusn(1+imdp/2:imdp  +iext,     2)
  zusn(1+imdp/2+iext:imdp+2*iext,       1)=zusn(1       :imdp/2+iext,     2)
  zusn(1            :imdp/2+iext,  jmdp+2)=zusn(1+imdp/2:imdp  +iext,jmdp+1)
  zusn(1+imdp/2+iext:imdp+2*iext,  jmdp+2)=zusn(1       :imdp/2+iext,jmdp+1)

!--- COMPUTE LIMITS OF MODEL GRIDPOINT AREA (REGULAR GRID)
  ALLOCATE(a(imar+1),b(imar+1))
  b(1:imar)=(x(1:imar  )+ x(2:imar+1))/2.0
  b(imar+1)= x(  imar+1)+(x(  imar+1)-x(imar))/2.0
  a(1)=x(1)-(x(2)-x(1))/2.0
  a(2:imar+1)= b(1:imar)

  ALLOCATE(c(jmar),d(jmar))
  d(1:jmar-1)=(y(1:jmar-1)+ y(2:jmar))/2.0
  d(  jmar  )= y(  jmar  )+(y(  jmar)-y(jmar-1))/2.0
  c(1)=y(1)-(y(2)-y(1))/2.0
  c(2:jmar)=d(1:jmar-1)

!--- INITIALIZATIONS:
  ALLOCATE(weight(imar+1,jmar)); weight(:,:)= 0.0
  ALLOCATE(zxtzx (imar+1,jmar)); zxtzx (:,:)= 0.0
  ALLOCATE(zytzy (imar+1,jmar)); zytzy (:,:)= 0.0
  ALLOCATE(zxtzy (imar+1,jmar)); zxtzy (:,:)= 0.0
  ALLOCATE(ztz   (imar+1,jmar)); ztz   (:,:)= 0.0
  zmea(:,:)= 0.0
  zpic(:,:)=-1.E+10
  zval(:,:)= 1.E+10

!--- COMPUTE SLOPES CORRELATIONS ON USN GRID
! CORRELATIONS OF USN OROGRAPHY GRADIENTS  ! dim (imdp+2*iext,jmdp+2)
  ALLOCATE(zytzyusn(imdp+2*iext,jmdp+2)); zytzyusn(:,:)=0.0
  ALLOCATE(zxtzxusn(imdp+2*iext,jmdp+2)); zxtzxusn(:,:)=0.0
  ALLOCATE(zxtzyusn(imdp+2*iext,jmdp+2)); zxtzyusn(:,:)=0.0
  DO j = 2, jmdp+1
    zdeltax=zdeltay*cos(yusn(j))
    DO i = 2, imdp+2*iext-1
      zytzyusn(i,j)=(zusn(i,j+1)-zusn(i,j-1))**2/zdeltay**2
      zxtzxusn(i,j)=(zusn(i+1,j)-zusn(i-1,j))**2/zdeltax**2
      zxtzyusn(i,j)=(zusn(i,j+1)-zusn(i,j-1))   /zdeltay  &
     &             *(zusn(i+1,j)-zusn(i-1,j))   /zdeltax
    END DO
  END DO

!--- SUMMATION OVER GRIDPOINT AREA
  zleny=xpi/REAL(jmdp)*rad
  xincr=xpi/REAL(jmdp)/2.
  ALLOCATE(num_tot(imar+1,jmar)); num_tot(:,:)=0.
  ALLOCATE(num_lan(imar+1,jmar)); num_lan(:,:)=0.
  DO ii = 1, imar+1
    DO jj = 1, jmar
      DO j = 2,jmdp+1 
        zlenx=zleny*COS(yusn(j))
        zdeltax=zdeltay*COS(yusn(j))
        weighy=(xincr+AMIN1(c(jj)-yusn(j),yusn(j)-d(jj)))*rad
        weighy=AMAX1(0.,AMIN1(weighy,zleny))

        IF(weighy==0.) CYCLE
        DO i = 2, imdp+2*iext-1
          weighx=(xincr+AMIN1(xusn(i)-a(ii),b(ii)-xusn(i)))*rad*COS(yusn(j))
          weighx=AMAX1(0.,AMIN1(weighx,zlenx))

          IF(weighx==0.) CYCLE
          num_tot(ii,jj)=num_tot(ii,jj)+1.0
          IF(zusn(i,j)>=1.)num_lan(ii,jj)=num_lan(ii,jj)+1.0
          weight(ii,jj)=weight(ii,jj)+weighx*weighy
          zxtzx(ii,jj)=zxtzx(ii,jj)+zxtzxusn(i,j)*weighx*weighy
          zytzy(ii,jj)=zytzy(ii,jj)+zytzyusn(i,j)*weighx*weighy
          zxtzy(ii,jj)=zxtzy(ii,jj)+zxtzyusn(i,j)*weighx*weighy
          ztz  (ii,jj)=  ztz(ii,jj)+zusn(i,j)*zusn(i,j)*weighx*weighy
          zmea (ii,jj)= zmea(ii,jj)+zusn(i,j)*weighx*weighy !--- MEAN
          zpic (ii,jj)=AMAX1(zpic(ii,jj),zusn(i,j))         !--- PEAKS
          zval (ii,jj)=AMIN1(zval(ii,jj),zusn(i,j))         !--- VALLEYS
        END DO
      END DO
    END DO
  END DO

!--- COMPUTE PARAMETERS NEEDED BY LOTT & MILLER (1997) AND LOTT (1999) SSO SCHEME
  IF(.NOT.masque_lu) THEN
    WHERE(weight(:,:)/=0.0) mask=num_lan(:,:)/num_tot(:,:)
  END IF
  nn=COUNT(weight(:,:)==0.0)
  IF(nn/=0) WRITE(lunout,*)'Problem with weight ; vanishing occurrences: ',nn
  WHERE(weight(:,:)/=0.0)
    zmea (:,:)=zmea (:,:)/weight(:,:)
    zxtzx(:,:)=zxtzx(:,:)/weight(:,:)
    zytzy(:,:)=zytzy(:,:)/weight(:,:)
    zxtzy(:,:)=zxtzy(:,:)/weight(:,:)
    ztz  (:,:)=ztz  (:,:)/weight(:,:)
    zstd (:,:)=ztz  (:,:)-zmea(:,:)**2
  END WHERE
  WHERE(zstd(:,:)<0) zstd(:,:)=0.
  zstd (:,:)=SQRT(zstd(:,:))

!--- CORRECT VALUES OF HORIZONTAL SLOPE NEAR THE POLES:
  zxtzx(:,   1)=zxtzx(:,     2)
  zxtzx(:,jmar)=zxtzx(:,jmar-1)
  zxtzy(:,   1)=zxtzy(:,     2)
  zxtzy(:,jmar)=zxtzy(:,jmar-1)
  zytzy(:,   1)=zytzy(:,     2)
  zytzy(:,jmar)=zytzy(:,jmar-1)

!=== FILTERS TO SMOOTH OUT FIELDS FOR INPUT INTO SSO SCHEME.
!--- FIRST FILTER, MOVING AVERAGE OVER 9 POINTS.
!-------------------------------------------------------------------------------
  zphi(:,:)=zmea(:,:)                           ! GK211005 (CG) UNSMOOTHED TOPO

  CALL MVA9(zmea);  CALL MVA9(zstd);  CALL MVA9(zpic);  CALL MVA9(zval)
  CALL MVA9(zxtzx); CALL MVA9(zxtzy); CALL MVA9(zytzy)

!--- MASK BASED ON GROUND MAXIMUM, 10% THRESHOLD. (SURFACE PARAMS MEANINGLESS)
  WHERE(weight(:,:)==0.0.OR.mask<0.1)
    zphi(:,:)=0.0; zmea(:,:)=0.0; zpic(:,:)=0.0; zval(:,:)=0.0; zstd(:,:)=0.0
  END WHERE
  DO ii = 1, imar
    DO jj = 1, jmar
      IF(weight(ii,jj)==0.0) CYCLE
    !--- Coefficients K, L et M:
      xk=(zxtzx(ii,jj)+zytzy(ii,jj))/2.
      xl=(zxtzx(ii,jj)-zytzy(ii,jj))/2.
      xm=zxtzy(ii,jj)
      xp=xk-SQRT(xl**2+xm**2)
      xq=xk+SQRT(xl**2+xm**2)
      xw=1.e-8
      IF(xp<=xw) xp=0.
      IF(xq<=xw) xq=xw
      IF(ABS(xm)<=xw) xm=xw*SIGN(1.,xm)
    !--- SLOPE, ANISOTROPY AND THETA ANGLE
      zsig(ii,jj)=SQRT(xq)
      zgam(ii,jj)=xp/xq
      zthe(ii,jj)=90.*ATAN2(xm,xl)/xpi
    END DO
  END DO
  WHERE(weight(:,:)==0.0.OR.mask<0.1)
    zsig(:,:)=0.0; zgam(:,:)=0.0; zthe(:,:)=0.0
  END WHERE

  WRITE(lunout,*)'  MEAN ORO:' ,MAXVAL(zmea)
  WRITE(lunout,*)'  ST. DEV.:' ,MAXVAL(zstd)
  WRITE(lunout,*)'  PENTE:'    ,MAXVAL(zsig)
  WRITE(lunout,*)'  ANISOTROP:',MAXVAL(zgam)
  WRITE(lunout,*)'  ANGLE:'    ,MINVAL(zthe),MAXVAL(zthe)
  WRITE(lunout,*)'  pic:'      ,MAXVAL(zpic)
  WRITE(lunout,*)'  val:'      ,MAXVAL(zval)
      
!--- Values at redundant longitude
  zmea(imar+1,:)=zmea(1,:)
  zphi(imar+1,:)=zphi(1,:)
  zpic(imar+1,:)=zpic(1,:)
  zval(imar+1,:)=zval(1,:)
  zstd(imar+1,:)=zstd(1,:)
  zsig(imar+1,:)=zsig(1,:)
  zgam(imar+1,:)=zgam(1,:)
  zthe(imar+1,:)=zthe(1,:)

!--- Values at north pole
  zweinor  =SUM(weight(1:imar,1))
  zmea(:,1)=SUM(weight(1:imar,1)*zmea(1:imar,1))/zweinor
  zphi(:,1)=SUM(weight(1:imar,1)*zphi(1:imar,1))/zweinor
  zpic(:,1)=SUM(weight(1:imar,1)*zpic(1:imar,1))/zweinor
  zval(:,1)=SUM(weight(1:imar,1)*zval(1:imar,1))/zweinor
  zstd(:,1)=SUM(weight(1:imar,1)*zstd(1:imar,1))/zweinor
  zsig(:,1)=SUM(weight(1:imar,1)*zsig(1:imar,1))/zweinor
  zgam(:,1)=1.; zthe(:,1)=0.

!--- Values at south pole
  zweisud     =SUM(weight(1:imar,jmar),DIM=1)
  zmea(:,jmar)=SUM(weight(1:imar,jmar)*zmea(1:imar,jmar))/zweisud
  zphi(:,jmar)=SUM(weight(1:imar,jmar)*zphi(1:imar,jmar))/zweisud
  zpic(:,jmar)=SUM(weight(1:imar,jmar)*zpic(1:imar,jmar))/zweisud
  zval(:,jmar)=SUM(weight(1:imar,jmar)*zval(1:imar,jmar))/zweisud
  zstd(:,jmar)=SUM(weight(1:imar,jmar)*zstd(1:imar,jmar))/zweisud
  zsig(:,jmar)=SUM(weight(1:imar,jmar)*zsig(1:imar,jmar))/zweisud
  zgam(:,jmar)=1.; zthe(:,jmar)=0.

END SUBROUTINE grid_noro
!
!-------------------------------------------------------------------------------


!-------------------------------------------------------------------------------
!
SUBROUTINE grid_noro0(xd,yd,zd,x,y,zphi,mask)
!
!===============================================================================
! Purpose: Extracted from grid_noro to provide geopotential height for dynamics
!          without any call to physics subroutines.
!===============================================================================
  IMPLICIT NONE 
!-------------------------------------------------------------------------------
! Arguments:
  REAL, INTENT(IN)  :: xd(:), yd(:) !--- INPUT  COORDINATES     (imdp) (jmdp)
  REAL, INTENT(IN)  :: zd(:,:)      !--- INPUT  FIELD           (imdp,  jmdp)
  REAL, INTENT(IN)  :: x(:), y(:)   !--- OUTPUT COORDINATES     (imar+1) (jmar)
  REAL, INTENT(OUT) :: zphi(:,:)    !--- GEOPOTENTIAL           (imar+1,jmar)
  REAL, INTENT(OUT) :: mask(:,:)    !--- MASK                   (imar+1,jmar)
!-------------------------------------------------------------------------------
! Local variables:
  CHARACTER(LEN=256) :: modname="grid_noro0"
  REAL, ALLOCATABLE :: xusn(:), yusn(:)           ! dim (imdp+2*iext) (jmdp+2)
  REAL, ALLOCATABLE :: zusn(:,:)                  ! dim (imdp+2*iext,  jmdp+2)
  REAL, ALLOCATABLE :: weight(:,:)                ! dim (imar+1,jmar)
  REAL, ALLOCATABLE :: num_tot(:,:), num_lan(:,:) ! dim (imar+1,jmar)
  REAL, ALLOCATABLE :: a(:), b(:)                 ! dim (imar+1)
  REAL, ALLOCATABLE :: c(:), d(:)                 ! dim (jmar)

  LOGICAL :: masque_lu
  INTEGER :: i, ii, imdp, imar, iext
  INTEGER :: j, jj, jmdp, jmar, nn
  REAL    :: xpi, zlenx, zleny, weighx, weighy, xincr, masque, rad

!-------------------------------------------------------------------------------
  imdp=assert_eq(SIZE(xd),SIZE(zd,1),TRIM(modname)//" imdp")
  jmdp=assert_eq(SIZE(yd),SIZE(zd,2),TRIM(modname)//" jmdp")
  imar=assert_eq(SIZE(x),SIZE(zphi,1),SIZE(mask,1),TRIM(modname)//" imar")-1
  jmar=assert_eq(SIZE(y),SIZE(zphi,2),SIZE(mask,2),TRIM(modname)//" jmar")
  iext=imdp/10
  xpi = ACOS(-1.)
  rad = 6371229.

!--- ARE WE USING A READ MASK ?
  masque_lu=ANY(mask/=-99999.); IF(.NOT.masque_lu) mask=0.0
  WRITE(lunout,*)'Masque lu: ',masque_lu

!--- EXTENSION OF THE INPUT DATABASE TO PROCEED COMPUTATIONS AT BOUNDARIES:
  ALLOCATE(xusn(imdp+2*iext))
  xusn(1     +iext:imdp  +iext)=xd(:)
  xusn(1          :       iext)=xd(1+imdp-iext:imdp)-2.*xpi
  xusn(1+imdp+iext:imdp+2*iext)=xd(1          :iext)+2.*xpi

  ALLOCATE(yusn(jmdp+2))
  yusn(1       )=yd(1)   +(yd(1)   -yd(2))
  yusn(2:jmdp+1)=yd(:)
  yusn(  jmdp+2)=yd(jmdp)+(yd(jmdp)-yd(jmdp-1))

  ALLOCATE(zusn(imdp+2*iext,jmdp+2))
  zusn(1       +iext:imdp  +iext,2:jmdp+1)=zd  (:                   ,     :)
  zusn(1            :       iext,2:jmdp+1)=zd  (imdp-iext+1:imdp    ,     :)
  zusn(1+imdp  +iext:imdp+2*iext,2:jmdp+1)=zd  (1:iext              ,     :)
  zusn(1            :imdp/2+iext,       1)=zusn(1+imdp/2:imdp  +iext,     2)
  zusn(1+imdp/2+iext:imdp+2*iext,       1)=zusn(1       :imdp/2+iext,     2)
  zusn(1            :imdp/2+iext,  jmdp+2)=zusn(1+imdp/2:imdp  +iext,jmdp+1)
  zusn(1+imdp/2+iext:imdp+2*iext,  jmdp+2)=zusn(1       :imdp/2+iext,jmdp+1)

!--- COMPUTE LIMITS OF MODEL GRIDPOINT AREA (REGULAR GRID)
  ALLOCATE(a(imar+1),b(imar+1))
  b(1:imar)=(x(1:imar  )+ x(2:imar+1))/2.0
  b(imar+1)= x(  imar+1)+(x(  imar+1)-x(imar))/2.0
  a(1)=x(1)-(x(2)-x(1))/2.0
  a(2:imar+1)= b(1:imar)

  ALLOCATE(c(jmar),d(jmar))
  d(1:jmar-1)=(y(1:jmar-1)+ y(2:jmar))/2.0
  d(  jmar  )= y(  jmar  )+(y(  jmar)-y(jmar-1))/2.0
  c(1)=y(1)-(y(2)-y(1))/2.0
  c(2:jmar)=d(1:jmar-1)

!--- INITIALIZATIONS:
  ALLOCATE(weight(imar+1,jmar)); weight(:,:)=0.0; zphi(:,:)=0.0

!--- SUMMATION OVER GRIDPOINT AREA
  zleny=xpi/REAL(jmdp)*rad
  xincr=xpi/REAL(jmdp)/2.
  ALLOCATE(num_tot(imar+1,jmar)); num_tot(:,:)=0.
  ALLOCATE(num_lan(imar+1,jmar)); num_lan(:,:)=0.
  DO ii = 1, imar+1
    DO jj = 1, jmar
      DO j = 2,jmdp+1 
        zlenx=zleny*COS(yusn(j))
        weighy=(xincr+AMIN1(c(jj)-yusn(j),yusn(j)-d(jj)))*rad
        weighy=AMAX1(0.,AMIN1(weighy,zleny))
        IF(weighy/=0) CYCLE
        DO i = 2, imdp+2*iext-1
          weighx=(xincr+AMIN1(xusn(i)-a(ii),b(ii)-xusn(i)))*rad*COS(yusn(j))
          weighx=AMAX1(0.,AMIN1(weighx,zlenx))
          IF(weighx/=0) CYCLE
          num_tot(ii,jj)=num_tot(ii,jj)+1.0
          IF(zusn(i,j)>=1.)num_lan(ii,jj)=num_lan(ii,jj)+1.0
          weight(ii,jj)=weight(ii,jj)+weighx*weighy
          zphi  (ii,jj)=zphi  (ii,jj)+zusn(i,j)*weighx*weighy !--- MEAN
        END DO
      END DO
    END DO
  END DO

!--- COMPUTE PARAMETERS NEEDED BY LOTT & MILLER (1997) AND LOTT (1999) SSO SCHEME
  IF(.NOT.masque_lu) THEN
    WHERE(weight(:,:)/=0.0) mask=num_lan(:,:)/num_tot(:,:)
  END IF
  nn=COUNT(weight(:,:)==0.0)
  IF(nn/=0) WRITE(lunout,*)'Problem with weight ; vanishing occurrences: ',nn
  WHERE(weight/=0.0) zphi(:,:)=zphi(:,:)/weight(:,:)

!--- MASK BASED ON GROUND MAXIMUM, 10% THRESHOLD (<10%: SURF PARAMS MEANINGLESS)
  WHERE(weight(:,:)==0.0.OR.mask<0.1) zphi(:,:)=0.0
  WRITE(lunout,*)'  MEAN ORO:' ,MAXVAL(zphi)

!--- Values at redundant longitude and at poles
  zphi(imar+1,:)=zphi(1,:)
  zphi(:,   1)=SUM(weight(1:imar,   1)*zphi(1:imar,   1))/SUM(weight(1:imar,   1))
  zphi(:,jmar)=SUM(weight(1:imar,jmar)*zphi(1:imar,jmar))/SUM(weight(1:imar,jmar))

END SUBROUTINE grid_noro0
!
!-------------------------------------------------------------------------------


!-------------------------------------------------------------------------------
!
SUBROUTINE read_noro(x,y,fname,zphi,zmea,zstd,zsig,zgam,zthe,zpic,zval,mask)
!
!-------------------------------------------------------------------------------
! Purpose: Read parameters usually determined with grid_noro from a file.
!===============================================================================
  USE netcdf, ONLY: NF90_OPEN,  NF90_INQ_DIMID, NF90_INQUIRE_DIMENSION,        &
        NF90_NOERR, NF90_CLOSE, NF90_INQ_VARID, NF90_GET_VAR, NF90_STRERROR,   &
        NF90_NOWRITE
  IMPLICIT NONE 
!-------------------------------------------------------------------------------
! Arguments:
  REAL, INTENT(IN)  :: x(:), y(:)    !--- OUTPUT COORDINATES     (imar+1) (jmar)
  CHARACTER(LEN=*), INTENT(IN) :: fname ! PARAMETERS FILE NAME
  REAL, INTENT(OUT) :: zphi(:,:)     !--- GEOPOTENTIAL           (imar+1,jmar)
  REAL, INTENT(OUT) :: zmea(:,:)     !--- MEAN OROGRAPHY         (imar+1,jmar)
  REAL, INTENT(OUT) :: zstd(:,:)     !--- STANDARD DEVIATION     (imar+1,jmar)
  REAL, INTENT(OUT) :: zsig(:,:)     !--- SLOPE                  (imar+1,jmar)
  REAL, INTENT(OUT) :: zgam(:,:)     !--- ANISOTROPY             (imar+1,jmar)
  REAL, INTENT(OUT) :: zthe(:,:)     !--- SMALL AXIS ORIENTATION (imar+1,jmar)
  REAL, INTENT(OUT) :: zpic(:,:)     !--- MAXIMUM ALTITUDE       (imar+1,jmar)
  REAL, INTENT(OUT) :: zval(:,:)     !--- MINIMUM ALTITUDE       (imar+1,jmar)
  REAL, INTENT(OUT) :: mask(:,:)     !--- MASK                   (imar+1,jmar)
!-------------------------------------------------------------------------------
! Local variables:
  CHARACTER(LEN=256) :: modname="read_noro"
  INTEGER :: imar, jmar, fid, did, vid
  LOGICAL :: masque_lu
  REAL :: xpi, d2r
!-------------------------------------------------------------------------------
  imar=assert_eq([SIZE(x),SIZE(zphi,1),SIZE(zmea,1),SIZE(zstd,1),SIZE(zsig,1), &
                          SIZE(zgam,1),SIZE(zthe,1),SIZE(zpic,1),SIZE(zval,1), &
                          SIZE(mask,1)],TRIM(modname)//" imar")-1
  jmar=assert_eq([SIZE(y),SIZE(zphi,2),SIZE(zmea,2),SIZE(zstd,2),SIZE(zsig,2), &
                          SIZE(zgam,2),SIZE(zthe,2),SIZE(zpic,2),SIZE(zval,2), &
                          SIZE(mask,2)],TRIM(modname)//" jmar")
  xpi=ACOS(-1.0); d2r=xpi/180.
  WRITE(lunout,*)"*** Orography parameters at sub-cell scale from file ***"

!--- ARE WE USING A READ MASK ?
  masque_lu=ANY(mask/=-99999.); IF(.NOT.masque_lu) mask=0.0
  WRITE(lunout,*)'Masque lu: ',masque_lu
  CALL ncerr(NF90_OPEN(fname,NF90_NOWRITE,fid))
  CALL check_dim('x','longitude',x(1:imar))
  CALL check_dim('y','latitude' ,y(1:jmar))
  IF(.NOT.masque_lu) CALL get_fld('mask',mask)
  CALL get_fld('Zphi',zphi)
  CALL get_fld('Zmea',zmea)
  CALL get_fld('mu'  ,zstd)
  CALL get_fld('Zsig',zsig)
  CALL get_fld('Zgam',zgam)
  CALL get_fld('Zthe',zthe)
  zpic=zmea+2*zstd
  zval=MAX(0.,zmea-2.*zstd)
  CALL ncerr(NF90_CLOSE(fid))
  WRITE(lunout,*)'  MEAN ORO:' ,MAXVAL(zmea)
  WRITE(lunout,*)'  ST. DEV.:' ,MAXVAL(zstd)
  WRITE(lunout,*)'  PENTE:'    ,MAXVAL(zsig)
  WRITE(lunout,*)'  ANISOTROP:',MAXVAL(zgam)
  WRITE(lunout,*)'  ANGLE:'    ,MINVAL(zthe),MAXVAL(zthe)
  WRITE(lunout,*)'  pic:'      ,MAXVAL(zpic)
  WRITE(lunout,*)'  val:'      ,MAXVAL(zval)

CONTAINS


SUBROUTINE get_fld(var,fld)
  CHARACTER(LEN=*), INTENT(IN)    :: var
  REAL,             INTENT(INOUT) :: fld(:,:)
  CALL ncerr(NF90_INQ_VARID(fid,var,vid),var)
  CALL ncerr(NF90_GET_VAR(fid,vid,fld(1:imar,:)),var)
  fld(imar+1,:)=fld(1,:)
END SUBROUTINE get_fld

SUBROUTINE check_dim(dimd,nam,dimv)
  CHARACTER(LEN=*), INTENT(IN) :: dimd
  CHARACTER(LEN=*), INTENT(IN) :: nam
  REAL,             INTENT(IN) :: dimv(:)
  REAL, ALLOCATABLE :: tmp(:)
  INTEGER :: n
  CALL ncerr(NF90_INQ_DIMID(fid,dimd,did))
  CALL ncerr(NF90_INQUIRE_DIMENSION(fid,did,len=n)); ALLOCATE(tmp(n))
  CALL ncerr(NF90_INQ_VARID(fid,dimd,did))
  CALL ncerr(NF90_GET_VAR(fid,did,tmp))
  IF(MAXVAL(tmp)>xpi) tmp=tmp*d2r
  IF(n/=SIZE(dimv).OR.ANY(ABS(tmp-dimv)>1E-6)) THEN
    WRITE(lunout,*)'Problem with file "'//TRIM(fname)//'".'
    CALL abort_physic(modname,'Grid differs from LMDZ for '//TRIM(nam)//'.',1)
  END IF
END SUBROUTINE check_dim

SUBROUTINE ncerr(ncres,var)
  IMPLICIT NONE
  INTEGER,          INTENT(IN) :: ncres
  CHARACTER(LEN=*), INTENT(IN), OPTIONAL :: var
  CHARACTER(LEN=256) :: mess
  IF(ncres/=NF90_NOERR) THEN
    mess='Problem with file "'//TRIM(fname)//'"'
    IF(PRESENT(var)) mess=TRIM(mess)//' and variable "'//TRIM(var)//'"'
    WRITE(lunout,*)TRIM(mess)//'.'
    CALL abort_physic(modname,NF90_STRERROR(ncres),1)
  END IF
END SUBROUTINE ncerr

END SUBROUTINE read_noro
!
!-------------------------------------------------------------------------------


!-------------------------------------------------------------------------------
!
SUBROUTINE MVA9(x)
!
!-------------------------------------------------------------------------------
  IMPLICIT NONE
! MAKE A MOVING AVERAGE OVER 9 GRIDPOINTS OF THE X FIELDS
!-------------------------------------------------------------------------------
! Arguments:
  REAL, INTENT(INOUT) :: x(:,:)
!-------------------------------------------------------------------------------
! Local variables:
  REAL    :: xf(SIZE(x,DIM=1),SIZE(x,DIM=2)), WEIGHTpb(-1:1,-1:1)
  INTEGER :: i, j, imar, jmar
!-------------------------------------------------------------------------------
  WEIGHTpb=RESHAPE([((1./REAL((1+i**2)*(1+j**2)),i=-1,1),j=-1,1)],SHAPE=[3,3])
  WEIGHTpb=WEIGHTpb/SUM(WEIGHTpb)
  imar=SIZE(X,DIM=1); jmar=SIZE(X,DIM=2)
  DO j=2,jmar-1
    DO i=2,imar-1
      xf(i,j)=SUM(x(i-1:i+1,j-1:j+1)*WEIGHTpb(:,:))
    END DO
  END DO
  DO j=2,jmar-1
    xf(1,j)=SUM(x(imar-1,j-1:j+1)*WEIGHTpb(-1,:))
    xf(1,j)=xf(1,j)+SUM(x(1:2,j-1:j+1)*WEIGHTpb(0:1,-1:1))
    xf(imar,j)=xf(1,j)
  END DO
  xf(:,   1)=xf(:,     2)
  xf(:,jmar)=xf(:,jmar-1)
  x(:,:)=xf(:,:)

END SUBROUTINE MVA9
!
!-------------------------------------------------------------------------------


END MODULE grid_noro_m



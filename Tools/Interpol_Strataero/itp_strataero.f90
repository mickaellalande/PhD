PROGRAM itp_strataero

  IMPLICIT NONE
  INCLUDE "netcdf.inc"

  INTEGER :: nyd, nys, nwav, nlev, nt
  INTEGER :: iret, fid, fidin, fidout, vid, vidin, vidout, dimid, natts
  INTEGER :: ivar, iatt, it, iw, il, iyd, iys
  REAL :: distmin, dist
  INTEGER, DIMENSION(4) :: dimids
  CHARACTER(LEN=200) :: gridfile, infile, outfile, attname, varname
  REAL, ALLOCATABLE, DIMENSION(:) :: yd, ys, lev, wav, time
  REAL, ALLOCATABLE, DIMENSION(:,:,:,:) :: varin, varout
  INTEGER, ALLOCATABLE, DIMENSION(:) :: iyclose

  CALL getarg(1,gridfile)

  iret = NF_OPEN(TRIM(gridfile),NF_NOWRITE,fid)
  CALL erreur(iret,.TRUE.,"open grid")
  iret = NF_INQ_VARID(fid,"latu",vid)
  CALL erreur(iret,.TRUE.,"inq latu")
  iret = NF_INQ_VARDIMID(fid,vid,dimids)
  CALL erreur(iret,.TRUE.,"inq vardimids")
  iret = NF_INQ_DIMLEN(fid,dimids(1),nyd)
  CALL erreur(iret,.TRUE.,"inq dimlen")
  ALLOCATE(yd(nyd))
  iret = NF_GET_VAR_REAL(fid,vid,yd)
  CALL erreur(iret,.TRUE.,"get var real")

  iret = NF_CLOSE(fid)
  CALL erreur(iret,.TRUE.,"close grid")

  CALL getarg(2,infile)
  CALL getarg(3,outfile)

  iret = NF_OPEN(TRIM(infile),NF_NOWRITE,fidin)
  CALL erreur(iret,.TRUE.,"open infile")
  iret = NF_INQ_VARID(fidin,"LAT",vid)
  CALL erreur(iret,.TRUE.,"inq LAT")
  iret = NF_INQ_VARDIMID(fidin,vid,dimids)
  CALL erreur(iret,.TRUE.,"inq vardimids")
  iret = NF_INQ_DIMLEN(fidin,dimids(1),nys)
  CALL erreur(iret,.TRUE.,"inq dimlen")
  ALLOCATE(ys(nys))
  iret = NF_GET_VAR_REAL(fidin,vid,ys)
  CALL erreur(iret,.TRUE.,"get var real")

  ALLOCATE(iyclose(nyd))
  DO iyd = 1, nyd
    iyclose(iyd) = -1
    distmin = 1.E20
    DO iys = 1, nys
      dist = ABS(yd(iyd)-ys(iys))
      IF ( dist .LT. distmin ) THEN
        distmin = dist
        iyclose(iyd) = iys
      ENDIF
    ENDDO
  ENDDO

  iret = NF_CREATE(TRIM(outfile),NF_CLOBBER,fidout)
  CALL erreur(iret,.TRUE.,"open outfile")

  varname = "LAT"
  iret = NF_DEF_DIM(fidout,TRIM(varname),nyd,dimids(1))
  CALL erreur(iret,.TRUE.,"def dim "//TRIM(varname))
  iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 1, dimids(1), vidout)
  CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  CALL erreur(iret,.TRUE.,"inq varid "//TRIM(varname))
  iret = NF_INQ_VARNATTS(fidin, vidin, natts)
  CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
  DO iatt = 1, natts
    iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
    iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
  ENDDO

  varname = "LEV"
  iret = NF_INQ_DIMID(fidin,TRIM(varname),dimid)
  CALL erreur(iret,.TRUE.,"inq dimid "//TRIM(varname))
  iret = NF_INQ_DIMLEN(fidin,dimid,nlev)
  CALL erreur(iret,.TRUE.,"inq dimlen "//TRIM(varname))
  iret = NF_DEF_DIM(fidout,TRIM(varname),nlev,dimids(2))
  CALL erreur(iret,.TRUE.,"def dim "//TRIM(varname))
  iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 1, dimids(2), vidout)
  CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  CALL erreur(iret,.TRUE.,"inq varid "//TRIM(varname))
  ALLOCATE(lev(nlev))
  iret = NF_GET_VAR_REAL(fidin,vidin,lev)
  CALL erreur(iret,.TRUE.,"get var real "//TRIM(varname))
  iret = NF_INQ_VARNATTS(fidin, vidin, natts)
  CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
  DO iatt = 1, natts
    iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
    iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
  ENDDO

  varname = "WAV"
  iret = NF_INQ_DIMID(fidin,TRIM(varname),dimid)
  CALL erreur(iret,.TRUE.,"inq dimid "//TRIM(varname))
  iret = NF_INQ_DIMLEN(fidin,dimid,nwav)
  CALL erreur(iret,.TRUE.,"inq dimlen "//TRIM(varname))
  iret = NF_DEF_DIM(fidout,"WAV",nwav,dimids(3))
  CALL erreur(iret,.TRUE.,"def dim "//TRIM(varname))
  iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 1, dimids(3), vidout)
  CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  CALL erreur(iret,.TRUE.,"inq varid "//TRIM(varname))
  ALLOCATE(wav(nwav))
  iret = NF_GET_VAR_REAL(fidin,vidin,wav)
  CALL erreur(iret,.TRUE.,"get var real "//TRIM(varname))
  iret = NF_INQ_VARNATTS(fidin, vidin, natts)
  CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
  DO iatt = 1, natts
    iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
    iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
  ENDDO

  varname = "TIME"
  iret = NF_INQ_DIMID(fidin,TRIM(varname),dimid)
  CALL erreur(iret,.TRUE.,"inq dimid "//TRIM(varname))
  iret = NF_INQ_DIMLEN(fidin,dimid,nt)
  CALL erreur(iret,.TRUE.,"inq dimlen "//TRIM(varname))
  iret = NF_DEF_DIM(fidout,"TIME",nt,dimids(4))
  CALL erreur(iret,.TRUE.,"def dim "//TRIM(varname))
  iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 1, dimids(4), vidout)
  CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  CALL erreur(iret,.TRUE.,"inq varid "//TRIM(varname))
  ALLOCATE(time(nt))
  iret = NF_GET_VAR_REAL(fidin,vidin,time)
  CALL erreur(iret,.TRUE.,"get var real "//TRIM(varname))
  iret = NF_INQ_VARNATTS(fidin, vidin, natts)
  CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
  DO iatt = 1, natts
    iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
    iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
  ENDDO

  varname = "TAU_EAR"
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  IF ( iret .EQ. 0 ) THEN
    iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 4, dimids, vidout)
    CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
    iret = NF_INQ_VARNATTS(fidin, vidin, natts)
    CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
    DO iatt = 1, natts
      iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
      iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
    ENDDO
  ENDIF

  varname = "TAU_SUN"
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  IF ( iret .EQ. 0 ) THEN
    iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 4, dimids, vidout)
    CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
    iret = NF_INQ_VARNATTS(fidin, vidin, natts)
    CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
    DO iatt = 1, natts
      iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
      iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
    ENDDO
  ENDIF

  varname = "OME_SUN"
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  IF ( iret .EQ. 0 ) THEN
    iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 4, dimids, vidout)
    CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
    iret = NF_INQ_VARNATTS(fidin, vidin, natts)
    CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
    DO iatt = 1, natts
      iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
      iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
    ENDDO
  ENDIF

  varname = "GGG_SUN"
  iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
  IF ( iret .EQ. 0 ) THEN
    iret = NF_DEF_VAR(fidout,TRIM(varname), NF_FLOAT, 4, dimids, vidout)
    CALL erreur(iret,.TRUE.,"def var "//TRIM(varname))
    iret = NF_INQ_VARNATTS(fidin, vidin, natts)
    CALL erreur(iret,.TRUE.,"inq varnatts "//TRIM(varname))
    DO iatt = 1, natts
      iret = NF_INQ_ATTNAME(fidin, vidin, iatt, attname)
      iret = NF_COPY_ATT(fidin,vidin,TRIM(attname),fidout,vidout)
    ENDDO
  ENDIF

  iret = NF_ENDDEF(fidout)
  CALL erreur(iret,.TRUE.,"enddef")

  iret = NF_INQ_VARID(fidout,"LAT",vidout)
  CALL erreur(iret,.TRUE.,"inq varid")
  iret = NF_PUT_VAR_REAL(fidout,vidout,yd)
  CALL erreur(iret,.TRUE.,"put var real")

  iret = NF_INQ_VARID(fidout,"LEV",vidout)
  CALL erreur(iret,.TRUE.,"inq varid")
  iret = NF_PUT_VAR_REAL(fidout,vidout,lev)
  CALL erreur(iret,.TRUE.,"put var real")

  iret = NF_INQ_VARID(fidout,"WAV",vidout)
  CALL erreur(iret,.TRUE.,"inq varid")
  iret = NF_PUT_VAR_REAL(fidout,vidout,wav)
  CALL erreur(iret,.TRUE.,"put var real")

  iret = NF_INQ_VARID(fidout,"TIME",vidout)
  CALL erreur(iret,.TRUE.,"inq varid")
  iret = NF_PUT_VAR_REAL(fidout,vidout,time)
  CALL erreur(iret,.TRUE.,"put var real")


  DO ivar = 1, 4

    IF ( ivar .EQ. 1 ) THEN
      varname = "TAU_EAR"
    ELSEIF ( ivar .EQ. 2 ) THEN
      varname = "TAU_SUN"
    ELSEIF ( ivar .EQ. 3 ) THEN
      varname = "OME_SUN"
    ELSEIF ( ivar .EQ. 4 ) THEN
      varname = "GGG_SUN"
    ELSE
      STOP 'devrait pas arriver'
    ENDIF

    iret = NF_INQ_VARID(fidin,TRIM(varname),vidin)
    IF ( iret .EQ. 0 ) THEN

      ALLOCATE(varin(nys,nlev,nwav,nt),varout(nyd,nlev,nwav,nt))
      iret = NF_GET_VAR_REAL(fidin,vidin,varin)
      CALL erreur(iret,.TRUE.,"get var real")
      DO it = 1, nt
      DO iw = 1, nwav
      DO il = 1, nlev
      DO iyd = 1, nyd
        varout(iyd,il,iw,it) = varin(iyclose(iyd),il,iw,it)
      ENDDO
      ENDDO
      ENDDO
      ENDDO

      iret = NF_INQ_VARID(fidout,TRIM(varname),vidout)
      CALL erreur(iret,.TRUE.,"inq varid "//TRIM(varname))
      iret = NF_PUT_VAR_REAL(fidout,vidout,varout)
      CALL erreur(iret,.TRUE.,"put var real "//TRIM(varname))

      DEALLOCATE(varin, varout)

    ENDIF

  ENDDO

  iret = NF_CLOSE(fidin)
  CALL erreur(iret,.TRUE.,"close infile")
  iret = NF_CLOSE(fidout)
  CALL erreur(iret,.TRUE.,"close outfile")

END PROGRAM itp_strataero

SUBROUTINE erreur(iret, lstop, chaine)
  ! pour les messages d'erreur
  INTEGER, INTENT(in)                     :: iret
  LOGICAL, INTENT(in)                     :: lstop
  CHARACTER(LEN=*), INTENT(in)            :: chaine
  !
  CHARACTER(LEN=256)                      :: message
  !
  INCLUDE "netcdf.inc"
  !
  IF ( iret .NE. 0 ) THEN
    WRITE(*,*) 'ROUTINE: ', TRIM(chaine)
    WRITE(*,*) 'ERREUR: ', iret
    message=NF_STRERROR(iret)
    WRITE(*,*) 'CA VEUT DIRE:',TRIM(message)
    IF ( lstop ) STOP
  ENDIF
  !
END SUBROUTINE erreur

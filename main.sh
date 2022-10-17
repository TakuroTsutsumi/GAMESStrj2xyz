#!/bin/bash
# Command: bash main.sh -f TS3_modNHC_IRCf.trj -b TS3_modNHC_IRCb.trj -c 5 

# Initial parameters
PYTHON3ROOT=""
FWDDATA="No--Data"
BWDDATA="No--Data"
HASFWD=0
HASBWD=0
# Initial parameters for Python
CUTTRJ=0  # STEP of cutted trajectory

# Argument parser: https://zenn.dev/kawarimidoll/articles/d546892a6d36eb
while (( $# > 0 ))
do
  case $1 in
    # ... Forward IRC, FWDDATA
	-f | --forward | --forward=*)
      if [[ "$1" =~ ^--forward= ]]; then
        FWDDATA=$(echo $1 | sed -e 's/^--forward=//')
      elif [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
        echo "'forward' requires an argument." 1>&2
        exit 1
      else
        FWDDATA="$2"
        shift
      fi
      ;;
    # ...

    # ... Backward IRC, BWDDATA
	-b | --backward | --backward=*)
      if [[ "$1" =~ ^--backward= ]]; then
        BWDDATA=$(echo $1 | sed -e 's/^--backward=//')
      elif [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
        echo "'backward' requires an argument." 1>&2
        exit 1
      else
        BWDDATA="$2"
        shift
      fi
      ;;
    # ...

    # ... Cut foward and backward IRCs, CUTTRJ
	-c | --cuttrj | --cuttrj=*)
      if [[ "$1" =~ ^--cuttrj= ]]; then
        CUTTRJ=$(echo $1 | sed -e 's/^--cuttrj=//')
      elif [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
        echo "'cuttrj' requires an argument." 1>&2
        exit 1
      else
        CUTTRJ="$2"
        shift
      fi
      ;;
    # ...
  esac
  shift
done

# Check FWD & BWD data
if [ -e $FWDDATA ]; then
    HASFWD=1
else
    HASFWD=0
fi

if [ -e $BWDDATA ]; then
    HASBWD=1
else
    HASBWD=0
fi


echo ""
echo "Start GAMESS-trj parser."


# Get NATOMS from FWDDATA
# Ex. NAT=      57 NFRG=       0 NQMMM=       0
NATOMS=$(head -n 2 ${FWDDATA} | grep "NAT=" | awk '{print $2}')

FILE_PARSER (){
	# Arguments
	#   $1 : hoge.trj
	#   $2 : 57 (# of atoms)
	#   $3 : 10 (Step of cutted trajectory)
	# Copy data
	DATANAME=$1
	DATANAME_TMP=$1__
	cp ${DATANAME}  ${DATANAME_TMP}
	# Delete several lines
	sed -i -e "/NAT=/d" ${DATANAME_TMP}
	sed -i -e "/----- QM PARTICLE COORDINATES/d" ${DATANAME_TMP}
	# Convert 2 lines into 1 line (Remove \n)
	sed -e ':a' -e 'N' -e '$!ba' -i -e "s/=====\n/===== /g" ${DATANAME_TMP}
	# Convert atomic names
	sed -i -e "s/PALLADIUM  46.0/Pd/g" ${DATANAME_TMP}
	sed -i -e "s/CARBON      6.0/ C/g" ${DATANAME_TMP}
	sed -i -e "s/NITROGEN    7.0/ P/g" ${DATANAME_TMP}
	sed -i -e "s/HYDROGEN    1.0/ H/g" ${DATANAME_TMP}
	sed -i -e "s/PHOSPHOROU 15.0/ P/g" ${DATANAME_TMP}
	# Grep xyz data
	DATAXYZ=${DATANAME%.*}.xyz
	grep -A $2 "IRC DATA PACKET FOR STEP" ${DATANAME_TMP} > ${DATAXYZ}
	sed -i -e "1i $2" ${DATAXYZ}
	sed -i -e "s/--/$2/g" ${DATAXYZ}
	sed -i -e "s/===== IRC DATA PACKET FOR //g" -e "s/=====//g" ${DATAXYZ}
	# Remove tmp file
	rm -rf ${DATANAME_TMP}

	if [ $3 -gt 0 ]; then
		# Reverse xyz file by Python
		${PYTHON3ROOT} xyz_cut.py ${DATAXYZ} -o ${DATAXYZ%.*}_cut${3}.xyz -s $3
		DATAXYZ=${DATAXYZ%.*}_cut${3}.xyz
	fi

	echo ${DATAXYZ}
}

# File parser
FWDXYZ="No--Data"
BWDXYZ="No--Data"

if [ $HASFWD -eq 1 ]; then
	echo "    Convert foward-trj into xyz."
	FWDXYZ=`FILE_PARSER ${FWDDATA} ${NATOMS} ${CUTTRJ}`

fi	

if [ $HASBWD -eq 1 ]; then
	echo "    Convert backward-trj into xyz."
	BWDXYZ=`FILE_PARSER ${BWDDATA} ${NATOMS} ${CUTTRJ}`
	# Reverse xyz file by Python
	${PYTHON3ROOT} xyz_reverse.py ${BWDXYZ} ${BWDXYZ%.*}_rev.xyz
	BWDXYZ=${BWDXYZ%.*}_rev.xyz
fi

if [ $HASBWD -eq 1 ] && [ $HASFWD -eq 1 ] ; then
	# Conbine xyz files by Python
	${PYTHON3ROOT} xyz_combine.py ${FWDXYZ} ${BWDXYZ} ${BWDXYZ%.*}_${FWDXYZ%.*}.xyz
fi

echo ""
echo "Finish GAMESS-trj parser."


#!/bin/bash



ROOT=${PWD}
STA_DIR=${ROOT}/statistics
RES_DIR=${ROOT}/results
MS_NAME="list_matrices.txt"
RE_NAME="list_executions.txt"



rm -f ${MS_NAME}
rm -f ${RE_NAME}



(
	cd ${STA_DIR}
	for FILE in *; do
		echo "${STA_DIR}/${FILE}" >> ${MS_NAME}
	done
	mv ${MS_NAME} ${ROOT}
)



(
	cd ${RES_DIR}
	for FILE in *; do
		echo "${RES_DIR}/${FILE}" >> ${RE_NAME}
	done
	mv ${RE_NAME} ${ROOT}
)




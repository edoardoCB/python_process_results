#!/usr/bin/env python




class MatrixInfo( object ):
	def __init__( self, name, spec ):
		self.name  = name
		self.nnz   = int(   spec['nnz']   )
		self.nrows = int(   spec['nrows'] )
		self.rmin  = int(   spec['rmin']  )
		self.rave  = float( spec['rave']  )
		self.rmax  = int(   spec['rmax']  )
		self.rsd   = float( spec['rsd']   )
		self.rsdp  = float( spec['rsdp']  )




class MatrixList( object ):
	def __init__( self, matrixListFile ):
		self.matrixListFile = matrixListFile
		self.matrixList     = dict()
		self.matrixReading()
		self.printMatrixListInfo()

	def matrixReading( self ):
		with open( self.matrixListFile, 'r' ) as mlf:
			for matrix in mlf:
				matrix = matrix.strip()
				with open( matrix, 'r' ) as file:
					while True:
						line = file.readline().strip().split()
						if not line: break
						if (line[0] == 'name:'):
							name = line[1]
							name = name[0:-4]
							break
					spec = dict()
					while True:
						line = file.readline().strip()
						if ':' in line:
							key, _, value     = line.partition(':')
							spec[key.strip()] = value.strip()
						if not line: break
					if not name in self.matrixList.keys(): self.matrixList[name] = MatrixInfo( name, spec )

	def printMatrixListInfo( self ):
		print ( '-------------------------------------------------------------------------' )
		print ( 'matrices\' info' )
		print ( '-------------------------------------------------------------------------' )
		print ( "{0:19s}   {1:7s}    {2:8s} {3:4s} {4:7s} {5:5s} {6:4s}    {7:8s}".format( 'matrix', 'nrows', 'nnz', 'rmin', 'rmax', 'rave', 'rsd', 'rsdp' ) )
		ml = self.matrixList
		for i in sorted( ml ):
			print ( "{0:19s} {1:7d} {2:8d}   {3:4d} {4:7d}   {5:5.1f} {6:4.1f} {7:8.1f}".format( i, ml[i].nrows, ml[i].nnz, ml[i].rmin, ml[i].rmax, ml[i].rave, ml[i].rsd, ml[i].rsdp ) )





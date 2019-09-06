#!/usr/bin/env python





class FormatInfo( object ):
	def __init__( self, formatName, mf, beta, tc ):
		self.formatName = formatName
		self.mf         = float( mf   )
		self.beta       = float( beta )
		self.tc         = float( tc   )





class KernelInfo( object ):
	def __init__( self, kernelName, flops, ordTime, aErr, rErr ):
		self.kernelName = kernelName
		self.flops      = float( flops     )
		self.ordTime    = float( ordTime   )
		self.aErr       = float( aErr      )
		self.rErr       = float( rErr      )





class ExecutionInfo( object ):
	def __init__( self, spec, formatList, kernelList, solverList ):
		self.matrix     = spec['matrix']
		self.run        = spec['run']
		self.hostname   = spec['hostname']
		self.srcFile    = spec['srcFile']
		self.hash       = spec['hash']
		self.date       = spec['date']
		self.ompNT      = spec['ompNT']
		self.ompSCH     = spec['ompSCH']
		self.mklNT      = spec['mklNT']
		self.numIte     = spec['numIte']
		self.formatList = formatList
		self.kernelList = kernelList
		self.solverList = solverList





class ExecutionList( object ):
	def __init__( self, executionListFile ):
		self.executionListFile = executionListFile
		self.executionList = []
		self.readExecutions()
		self.printSettings()
		self.formatDataTuple = {}
		self.readFormatData()
		self.bestKernelPerformancesTuple = {}
		self.readBestKernelPerformances()
		self.bestKernelPerformerDict = dict()
		self.getBestKernelPerformer()
		self.bestKernelPerformerDict_AX = dict()
		self.getBestKernelPerformer_AX()
		self.bestKernelPerformerDict_NOTAX = dict()
		self.getBestKernelPerformer_NOTAX()
		self.calculatePercentage()
		self.printFormatData()
		self.printKernelPerformances()
		self.printKernelAbsErr()
		self.printKernelRelErr()

	def readExecutions( self ):
		with open( self.executionListFile, 'r' ) as elf:
			for execution in elf:
				execution = execution.strip()
				run       = execution[-21:-11]
				numLines  = sum( 1 for line in open( execution, 'r' ) )
				dict1     = dict()
				list1     = []
				list2     = []
				list3     = []
				with open( execution, 'r' ) as f:
					for i in range( numLines ):
						l = f.readline().strip().split()
						if ( len(l) == 2 ) and ( l[0] == 'matFileName:' ):
							word            = l[1]
							dict1['matrix'] = word[0:-4]
							dict1['run']    = run
						if ( len(l) == 2 ) and ( l[0] == 'hbs:'                   ): dict1['hbs']       = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'CHUNK_SIZE:'            ): dict1['chunkSize'] = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'hostname:'              ): dict1['hostname']  = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'srcFileName:'           ): dict1['srcFile']   = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'gitHash:'               ): dict1['hash']      = l[1]
						if ( len(l) == 3 ) and ( l[0] == 'date:'                  ): dict1['date']      = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'ompMaxThreads:'         ): dict1['ompNT']     = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'omp_schedule:'          ): dict1['ompSCH']    = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'mklMaxThreads:'         ): dict1['mklNT']     = l[1]
						if ( len(l) == 2 ) and ( l[0] == 'NUM_ITE:'               ): dict1['numIte']    = l[1]
						if ( len(l) == 4 ) and ( l[0] == 'f_csr'                  ): list1.append( FormatInfo( 'fcsr',         l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_k1'                   ): list1.append( FormatInfo( 'fk1',          l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axc'                  ): list1.append( FormatInfo( 'faxc',         l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h1_hw8'       ): list1.append( FormatInfo( 'faxtuh1',      l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h4_hw8'       ): list1.append( FormatInfo( 'faxtuh4',      l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h8_hw8'       ): list1.append( FormatInfo( 'faxtuh8',      l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h12_hw8'      ): list1.append( FormatInfo( 'faxtuh12',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h16_hw8'      ): list1.append( FormatInfo( 'faxtuh16',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h20_hw8'      ): list1.append( FormatInfo( 'faxtuh20',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h24_hw8'      ): list1.append( FormatInfo( 'faxtuh24',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h28_hw8'      ): list1.append( FormatInfo( 'faxtuh28',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h32_hw8'      ): list1.append( FormatInfo( 'faxtuh32',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h36_hw8'      ): list1.append( FormatInfo( 'faxtuh36',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_unc_h40_hw8'      ): list1.append( FormatInfo( 'faxtuh40',     l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_com_h1_hw8_bs64'  ): list1.append( FormatInfo( 'faxtch1bs64',  l[1], l[2], l[3] ) )
						if ( len(l) == 4 ) and ( l[0] == 'f_axt_com_h1_hw8_bs512' ): list1.append( FormatInfo( 'faxtch1bs512', l[1], l[2], l[3] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_naive_csr'            ): list2.append( KernelInfo( 'pcsr1',        l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_mkl_sparse_insp_csr'  ): list2.append( KernelInfo( 'pcsr2',        l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_k1'                   ): list2.append( KernelInfo( 'pk1',          l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_k1p'                  ): list2.append( KernelInfo( 'pk1p',         l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axc'                  ): list2.append( KernelInfo( 'paxc',         l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h1_hw8'       ): list2.append( KernelInfo( 'paxtuh1',      l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h4_hw8'       ): list2.append( KernelInfo( 'paxtuh4',      l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h8_hw8'       ): list2.append( KernelInfo( 'paxtuh8',      l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h12_hw8'      ): list2.append( KernelInfo( 'paxtuh12',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h16_hw8'      ): list2.append( KernelInfo( 'paxtuh16',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h20_hw8'      ): list2.append( KernelInfo( 'paxtuh20',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h24_hw8'      ): list2.append( KernelInfo( 'paxtuh24',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h28_hw8'      ): list2.append( KernelInfo( 'paxtuh28',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h32_hw8'      ): list2.append( KernelInfo( 'paxtuh32',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h36_hw8'      ): list2.append( KernelInfo( 'paxtuh36',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_unc_h40_hw8'      ): list2.append( KernelInfo( 'paxtuh40',     l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_com_h1_hw8_bs64'  ): list2.append( KernelInfo( 'paxtch1bs64',  l[2], l[3], l[4], l[5] ) )
						if ( len(l) == 7 ) and ( l[0] == 'p_axt_com_h1_hw8_bs512' ): list2.append( KernelInfo( 'paxtch1bs512', l[2], l[3], l[4], l[5] ) )
				self.executionList.append( ExecutionInfo( dict1, list1, list2, list3 ) )

	def printSettings( self ):
		print( '------------------------------------------------------------------------------------------------------------' )
		print( 'useful information'                                                                                           )
		print( '------------------------------------------------------------------------------------------------------------' )
		print( 'hostname:          {0:48s}'.format( self.executionList[0].hostname )                                          )
		print( 'srcFile:           {0:48s}'.format( self.executionList[0].srcFile  )                                          )
		print( 'hash:              {0:48s}'.format( self.executionList[0].hash     )                                          )
		print( 'date (yyyy-mm-dd): {0:48s}'.format( self.executionList[0].date     )                                          )
		print( 'ompMaxThreads:     {0:48s}'.format( self.executionList[0].ompNT    )                                          )
		print( 'ompSchedule:       {0:48s}'.format( self.executionList[0].ompSCH   )                                          )
		print( 'mklMaxThreads:     {0:48s}'.format( self.executionList[0].mklNT    )                                          )
		print( 'numIte:            {0:48s}'.format( self.executionList[0].numIte   )                                          )
		print( 'pcsr1:             naive implementation of CSR'                                                               )
		print( 'pcsr2:             MKL function for CSR format (using optimization)'                                          )
		print( 'pk1:               original kernel for K1 or SELL-C-alpha format'                                             )
		print( 'pk1p:              my modified kernel for K1 or SELL-C-alpha format'                                          )
		print( 'paxc:              old proposal (it\'s already published)'                                                    )
		print( 'paxtuh*:           new proposal (AXT, mode = uncompacted, tileHeight = *, tileHalfWidth = 8)'                 )
		print( 'paxtch*bs**:       new proposal (AXT, mode = compacted,   tileHeight = *, tileHalfWidth = 8, blockSize = **)' )

	def readFormatData( self ):
		tupleFD = {}
		for e in self.executionList:
			for k in e.formatList:
				ck = ( e.matrix, k.formatName )
				m  = k.mf
				o  = k.beta
				t  = k.tc
				v  = ( m, o, t )
				if not ck in tupleFD:
					tupleFD[ck] = v
				else:
					if ( t < tupleFD[ck][2] ):
						tupleFD[ck] = v
		self.formatDataTuple = tupleFD

	def readBestKernelPerformances( self ):
		tupleBKP = {}
		for e in self.executionList:
			for k in e.kernelList:
				ck = ( e.matrix, k.kernelName )
				pe  = k.flops
				ae  = k.aErr
				re  = k.rErr
				v   = ( pe, ae, re )
				if not ck in tupleBKP:
					tupleBKP[ck] = v
				else:
					if ( v[0] > tupleBKP[ck][0] ):
						tupleBKP[ck] = v
		self.bestKernelPerformancesTuple = tupleBKP

	def getBestKernelPerformer( self ):
		bkpt  = self.bestKernelPerformancesTuple
		dict1 = dict()
		for ( ck, cv ) in sorted( bkpt.items() ):
			if not ck[0] in dict1:
				dict1[ ck[0] ] = ( ck[1], cv[0], cv[1], cv[2] )
			else:
				valueOnDict1 = dict1[ ck[0] ][1]
				if cv[0] > valueOnDict1:
					dict1[ ck[0] ] = ( ck[1], cv[0], cv[1], cv[2] )
		self.bestKernelPerformerDict = dict1

	def getBestKernelPerformer_AX( self ):
		bkpt  = self.bestKernelPerformancesTuple
		dict1 = dict()
		for ( ck, cv ) in sorted( bkpt.items() ):
			if (ck[1]!='pcsr1') and (ck[1]!='pcsr2') and (ck[1]!='pk1') and (ck[1]!='pk1p'):
				dict1[ ck ] = cv
		dict2 = dict()
		for ( ck, cv ) in sorted( dict1.items() ):
			if not ck[0] in dict2:
				dict2[ ck[0] ] = ( ck[1], cv[0], cv[1], cv[2] )
			else:
				valueOnDict2 = dict2[ ck[0] ][1]
				if cv[0] > valueOnDict2:
					dict2[ ck[0] ] = ( ck[1], cv[0], cv[1], cv[2] )
		self.bestKernelPerformerDict_AX = dict2

	def getBestKernelPerformer_NOTAX( self ):
		bkpt  = self.bestKernelPerformancesTuple
		dict1 = dict()
		for ( ck, cv ) in sorted( bkpt.items() ):
			if (ck[1]=='pcsr1') or (ck[1]=='pcsr2') or (ck[1]=='pk1') or (ck[1]=='pk1p'):
				dict1[ ck ] = cv
		dict2 = dict()
		for ( ck, cv ) in sorted( dict1.items() ):
			if not ck[0] in dict2:
				dict2[ ck[0] ] = ( ck[1], cv[0], cv[1], cv[2] )
			else:
				valueOnDict2 = dict2[ ck[0] ][1]
				if cv[0] > valueOnDict2:
					dict2[ ck[0] ] = ( ck[1], cv[0], cv[1], cv[2] )
		self.bestKernelPerformerDict_NOTAX = dict2

	def calculatePercentage( self ):
		dict1 = self.bestKernelPerformerDict_NOTAX
		dict2 = self.bestKernelPerformerDict_AX
		dict3 = dict()
		for ( ck1, cv1 ) in sorted( dict1.items() ):
			cv2 = dict2[ ck1 ]
			percentage = ( cv2[1] - cv1[1] ) / cv1[1]
			percentage = percentage * 100
			dict3[ ck1 ] = percentage
		self.percentageDict = dict3

	def printFormatData( self ):
		fdt = self.formatDataTuple
		m   = {}
		m   = [ ck[0] for ( ck, cv ) in sorted( fdt.items() ) if not ck[0] in m ]
		f1  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'fcsr'        ]
		f2  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'fk1'         ]
		f3  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxc'        ]
		f4  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh1'     ]
		f5  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh4'     ]
		f6  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh8'     ]
		f7  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh12'    ]
		f8  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh16'    ]
		f9  = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh20'    ]
		f10 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh24'    ]
		f11 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh28'    ]
		f12 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh32'    ]
		f13 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh36'    ]
		f14 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtuh40'    ]
		f15 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtch1bs64' ]
		f16 = [ cv for ( ck, cv ) in sorted( fdt.items() ) if ck[1] == 'faxtch1bs512' ]
		f   = 16
		print( '-----------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print( 'formats\' data' )
		print( '-----------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print( '***** memory footprint [MB] *****' )
		print( "{0:19s}   {1:9s} {2:9s} {3:9s} {4:9s} {5:9s} {6:9s} {7:9s} {8:9s} {9:9s} {10:9s} {11:9s} {12:9s} {13:9s} {14:9s} {15:9s} {16:9s}".format( 'matrix', 'fcsr     ', 'fk1      ', 'faxc     ', 'faxtuh1  ', 'faxtuh4  ', 'faxtuh8  ', 'faxtuh12 ', 'faxtuh16 ', 'faxtuh20 ', 'faxtuh24 ', 'faxtuh28 ', 'faxtuh32 ', 'faxtuh36 ', 'faxtuh40 ', 'faxtch1bs64', 'faxtch1bs512' ) )
		for i in range( len(f1) ):
			print ( "{0:19s} {1:9.1f} {2:9.1f} {3:9.1f} {4:9.1f} {5:9.1f} {6:9.1f} {7:9.1f} {8:9.1f} {9:9.1f} {10:9.1f} {11:9.1f} {12:9.1f} {13:9.1f} {14:9.1f} {15:9.1f} {16:9.1f}".format( m[i*f], f1[i][0], f2[i][0], f3[i][0], f4[i][0], f5[i][0], f6[i][0], f7[i][0], f8[i][0], f9[i][0], f10[i][0], f11[i][0], f12[i][0], f13[i][0], f14[i][0], f15[i][0], f16[i][0] ) )
		print ( '***** occupancy *****' )
		print( "{0:19s}   {1:9s} {2:9s} {3:9s} {4:9s} {5:9s} {6:9s} {7:9s} {8:9s} {9:9s} {10:9s} {11:9s} {12:9s} {13:9s} {14:9s} {15:9s} {16:9s}".format( 'matrix', 'fcsr     ', 'fk1      ', 'faxc     ', 'faxtuh1  ', 'faxtuh4  ', 'faxtuh8  ', 'faxtuh12 ', 'faxtuh16 ', 'faxtuh20 ', 'faxtuh24 ', 'faxtuh28 ', 'faxtuh32 ', 'faxtuh36 ', 'faxtuh40 ', 'faxtch1bs64', 'faxtch1bs512' ) )
		for i in range( len(f1) ):
			print ( "{0:19s} {1:9.2f} {2:9.2f} {3:9.2f} {4:9.2f} {5:9.2f} {6:9.2f} {7:9.2f} {8:9.2f} {9:9.2f} {10:9.2f} {11:9.2f} {12:9.2f} {13:9.2f} {14:9.2f} {15:9.2f} {16:9.2f}".format( m[i*f], f1[i][1], f2[i][1], f3[i][1], f4[i][1], f5[i][1], f6[i][1], f7[i][1], f8[i][1], f9[i][1], f10[i][1], f11[i][1], f12[i][1], f13[i][1], f14[i][1], f15[i][1], f16[i][1] ) )
		print ( '***** conversion time [s] *****' )
		print( "{0:19s}   {1:9s} {2:9s} {3:9s} {4:9s} {5:9s} {6:9s} {7:9s} {8:9s} {9:9s} {10:9s} {11:9s} {12:9s} {13:9s} {14:9s} {15:9s} {16:9s}".format( 'matrix', 'fcsr     ', 'fk1      ', 'faxc     ', 'faxtuh1  ', 'faxtuh4  ', 'faxtuh8  ', 'faxtuh12 ', 'faxtuh16 ', 'faxtuh20 ', 'faxtuh24 ', 'faxtuh28 ', 'faxtuh32 ', 'faxtuh36 ', 'faxtuh40 ', 'faxtch1bs64', 'faxtch1bs512' ) )
		for i in range( len(f1) ):
			print ( "{0:19s} {1:9.6f} {2:9.6f} {3:9.6f} {4:9.6f} {5:9.6f} {6:9.6f} {7:9.6f} {8:9.6f} {9:9.6f} {10:9.6f} {11:9.6f} {12:9.6f} {13:9.6f} {14:9.6f} {15:9.6f} {16:9.6f}".format( m[i*f], f1[i][2], f2[i][2], f3[i][2], f4[i][2], f5[i][2], f6[i][2], f7[i][2], f8[i][2], f9[i][2], f10[i][2], f11[i][2], f12[i][2], f13[i][2], f14[i][2], f15[i][2], f16[i][2] ) )

	def printKernelPerformances( self ):
		bkpt       = self.bestKernelPerformancesTuple
		m          = {}
		m          = [ ck[0] for ( ck, cv ) in sorted( bkpt.items() ) if not ck[0] in m ]
		k1         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pcsr1'        ]
		k2         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pcsr2'        ]
		k3         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pk1'          ]
		k4         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pk1p'         ]
		k5         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxc'         ]
		k6         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh1'      ]
		k7         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh4'      ]
		k8         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh8'      ]
		k9         = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh12'     ]
		k10        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh16'     ]
		k11        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh20'     ]
		k12        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh24'     ]
		k13        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh28'     ]
		k14        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh32'     ]
		k15        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh36'     ]
		k16        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh40'     ]
		k17        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtch1bs64'  ]
		k18        = [ cv[0] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtch1bs512' ]
		f          = 18
		bkpd       = self.bestKernelPerformerDict
		bkpd_ax    = self.bestKernelPerformerDict_AX
		bkpd_notax = self.bestKernelPerformerDict_NOTAX
		p          = self.percentageDict
		print( '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print( 'kernels\' performance [GFLOPS]' )
		print( '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print ( "{0:19s}     {1:9s} {2:9s} {3:9s} {4:9s} {5:9s} {6:9s} {7:9s} {8:9s} {9:9s} {10:9s} {11:9s} {12:9s} {13:9s} {14:9s} {15:9s} {16:9s} {17:9s} {18:9s}".format( 'matrix', 'pcsr1    ', 'pcsr2    ', 'pk1      ', 'pk1p     ', 'paxc     ', 'paxtuh1  ', 'paxtuh4  ', 'paxtuh8  ', 'paxtuh12 ', 'paxtuh16 ', 'paxtuh20 ', 'paxtuh24 ', 'paxtuh28 ', 'paxtuh32 ', 'paxtuh36 ', 'paxtuh40 ', 'paxtch1bs64', 'paxtch1bs512' ) )
		for i in range( len(k1) ):
			print( "{0:19s} {1:9.1f} {2:9.1f} {3:9.1f} {4:9.1f} {5:9.1f} {6:9.1f} {7:9.1f} {8:9.1f} {9:9.1f} {10:9.1f} {11:9.1f} {12:9.1f} {13:9.1f} {14:9.1f} {15:9.1f} {16:9.1f} {17:9.1f} {18:9.1f}".format( m[i*f], k1[i], k2[i], k3[i], k4[i], k5[i], k6[i], k7[i], k8[i], k9[i], k10[i], k11[i], k12[i], k13[i], k14[i], k15[i], k16[i], k17[i], k18[i] ) )
		print( '***** synthesis ***** (negative percentage indicates cases where a non AX based format is the best)' )
		print ( "{0:19s} {1:13s} {2:13s} {3:13s}   {4:13s}".format( 'matrix', 'bestPerformer', 'best_AX      ', 'best_NOT_AX  ', 'percentage   ' ) )
		for i in range( len(k1) ):
			print( "{0:19s} {1:13s} {2:13s} {3:13s} {4:13.1f}".format( m[i*f], bkpd[m[i*f]][0], bkpd_ax[m[i*f]][0], bkpd_notax[m[i*f]][0], p[m[i*f]] ) )

	def printKernelAbsErr( self ):
		bkpt = self.bestKernelPerformancesTuple
		m    = {}
		m    = [ ck[0] for ( ck, cv ) in sorted( bkpt.items() ) if not ck[0] in m ]
		k1   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pcsr1'        ]
		k2   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pcsr2'        ]
		k3   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pk1'          ]
		k4   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pk1p'         ]
		k5   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxc'         ]
		k6   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh1'      ]
		k7   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh4'      ]
		k8   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh8'      ]
		k9   = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh12'     ]
		k10  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh16'     ]
		k11  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh20'     ]
		k12  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh24'     ]
		k13  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh28'     ]
		k14  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh32'     ]
		k15  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh36'     ]
		k16  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh40'     ]
		k17  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtch1bs64'  ]
		k18  = [ cv[1] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtch1bs512' ]
		f    = 18
		print( '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print( 'kernels\' absolute error' )
		print( '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print ( "{0:19s}     {1:9s} {2:9s} {3:9s} {4:9s} {5:9s} {6:9s} {7:9s} {8:9s} {9:9s} {10:9s} {11:9s} {12:9s} {13:9s} {14:9s} {15:9s} {16:9s} {17:9s} {18:9s}".format( 'matrix', 'pcsr1    ', 'pcsr2    ', 'pk1      ', 'pk1p     ', 'paxc     ', 'paxtuh1  ', 'paxtuh4  ', 'paxtuh8  ', 'paxtuh12 ', 'paxtuh16 ', 'paxtuh20 ', 'paxtuh24 ', 'paxtuh28 ', 'paxtuh32 ', 'paxtuh36 ', 'paxtuh40 ', 'paxtch1bs64', 'paxtch1bs512' ) )
		for i in range( len(k1) ):
			print( "{0:19s} {1:9.1e} {2:9.1e} {3:9.1e} {4:9.1e} {5:9.1e} {6:9.1e} {7:9.1e} {8:9.1e} {9:9.1e} {10:9.1e} {11:9.1e} {12:9.1e} {13:9.1e} {14:9.1e} {15:9.1e} {16:9.1e} {17:9.1e} {18:9.1e}".format( m[i*f], k1[i], k2[i], k3[i], k4[i], k5[i], k6[i], k7[i], k8[i], k9[i], k10[i], k11[i], k12[i], k13[i], k14[i], k15[i], k16[i], k17[i], k18[i] ) )

	def printKernelRelErr( self ):
		bkpt = self.bestKernelPerformancesTuple
		m    = {}
		m    = [ ck[0] for ( ck, cv ) in sorted( bkpt.items() ) if not ck[0] in m ]
		k1   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pcsr1'       ]
		k2   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pcsr2'       ]
		k3   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pk1'         ]
		k4   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'pk1p'        ]
		k5   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxc'        ]
		k6   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh1'     ]
		k7   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh4'     ]
		k8   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh8'     ]
		k9   = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh12'    ]
		k10  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh16'    ]
		k11  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh20'    ]
		k12  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh24'    ]
		k13  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh28'    ]
		k14  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh32'    ]
		k15  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh36'    ]
		k16  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtuh40'    ]
		k17  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtch1bs64' ]
		k18  = [ cv[2] for ( ck, cv ) in sorted( bkpt.items() ) if ck[1] == 'paxtch1bs512' ]
		f    = 18
		print( '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print( 'kernels\' relative error' )
		print( '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' )
		print ( "{0:19s}     {1:9s} {2:9s} {3:9s} {4:9s} {5:9s} {6:9s} {7:9s} {8:9s} {9:9s} {10:9s} {11:9s} {12:9s} {13:9s} {14:9s} {15:9s} {16:9s} {17:9s} {18:9s}".format( 'matrix', 'pcsr1    ', 'pcsr2    ', 'pk1      ', 'pk1p     ', 'paxc     ', 'paxtuh1  ', 'paxtuh4  ', 'paxtuh8  ', 'paxtuh12 ', 'paxtuh16 ', 'paxtuh20 ', 'paxtuh24 ', 'paxtuh28 ', 'paxtuh32 ', 'paxtuh36 ', 'paxtuh40 ', 'paxtch1bs64', 'paxtch1bs512' ) )
		for i in range( len(k1) ):
			print( "{0:19s} {1:9.1e} {2:9.1e} {3:9.1e} {4:9.1e} {5:9.1e} {6:9.1e} {7:9.1e} {8:9.1e} {9:9.1e} {10:9.1e} {11:9.1e} {12:9.1e} {13:9.1e} {14:9.1e} {15:9.1e} {16:9.1e} {17:9.1e} {18:9.1e}".format( m[i*f], k1[i], k2[i], k3[i], k4[i], k5[i], k6[i], k7[i], k8[i], k9[i], k10[i], k11[i], k12[i], k13[i], k14[i], k15[i], k16[i], k17[i], k18[i] ) )






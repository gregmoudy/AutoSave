""" Core of the auto save module. """

import glob
import os
import tempfile
import time
import wx


DIR_AUTO_SAVE = os.path.join( tempfile.gettempdir( ), 'auto_save_test' )
MAX_AUTO_SAVES = 10
AUTO_SAVE_INTERVAL = 1000 # In miliseconds
AUTO_SAVE_FILENAME_TEMPLATE = os.path.join( DIR_AUTO_SAVE, 'auto_save_' ) + '{0}.bak'


class AutoSaver( wx.Timer ):
	def __init__( self, save_func, *args, **kwargs ):
		super( ).__init__( *args, **kwargs )

		# Save function to be called at the end of auto saver timer. Save function should take a single argument of the full file path to save to.
		self._save_func = save_func

		# Create the directory for the auto save files if it does not already exist.
		if not os.path.exists( DIR_AUTO_SAVE ):
			os.mkdir( DIR_AUTO_SAVE )


	def start( self ):
		self.Start( AUTO_SAVE_INTERVAL )


	def stop( self ):
		self.Stop( )


	def get_auto_save_file( self ):
		# Generate a list of the potential auto save filenames.
		potential_auto_save_files = [ AUTO_SAVE_FILENAME_TEMPLATE.format( x ) for x in range( MAX_AUTO_SAVES ) ]

		# Generate a list of auto save file names from the potentials list that currently exist.
		current_auto_save_files = glob.glob( AUTO_SAVE_FILENAME_TEMPLATE.format( '*' ) )
		current_auto_save_files = [ x for x in current_auto_save_files if x in potential_auto_save_files ]

		# If the list of current auto saves matches the limit of the number of auto save files maintained...
		if len( current_auto_save_files ) == MAX_AUTO_SAVES:
			# Sort the current list by modified date and use the first one which should be the oldest file.
			current_auto_save_files.sort( key = os.path.getmtime )
			full_local_filename = current_auto_save_files[ 0 ]

		# Otherwise...
		else:
			# Get a list of which file names are still available to be written to for the first time and use the first one.
			available_auto_save_files = [ x for x in potential_auto_save_files if x not in current_auto_save_files ]
			full_local_filename = available_auto_save_files[ 0 ]

		return full_local_filename


	def Notify( self ):
		# Get the full local filename of the auto save file to write to.
		full_local_filename = self.get_auto_save_file( )

		print( '{0} - {1}'.format( time.ctime( ), full_local_filename ) )

		self._save_func( full_local_filename )

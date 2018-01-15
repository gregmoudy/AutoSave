""" Demo application of the auto save module. """

import wx

import auto_save


class DemoFrame( wx.Frame ):
	def __init__( self, *args, **kwargs ):
		super( ).__init__( *args, **kwargs )

		self._auto_saver = auto_save.AutoSaver( save_func = test_save_func )
		self._auto_saver.start( )

		self.Bind( wx.EVT_CLOSE, self.on_close )


	def on_close( self, event ):
		self._auto_saver.stop( )
		event.Skip( )



def test_save_func( full_local_filename ):
	with open( full_local_filename, 'w' ) as test_file:
		print( 'test', file = test_file )



if __name__ == '__main__':
	app = wx.App( )
	frame = DemoFrame( None, title = 'Auto Save Test App' )
	frame.Show( )
	app.MainLoop()

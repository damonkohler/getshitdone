If you're looking for a no nonsense way to whip up a web app in a hurry, you've found it.

Source lines of code: 72

A GSD web app is defined by subclassing gsd.App. There are no explicit URL mappings. Instead, methods that begin with 'GET' will be called based on the URL. For example, http://localhost/foo/bar will call the 'GET\_foo\_bar()' method. Templates are defined by simply using '<?...?>' to contain pure Python code. The code snippets are evaluated in a specified scope when the template is rendered. To start serving the application, instantiate the class and call the instance's 'Serve()' method.

Check out the [super simple example](http://code.google.com/p/getshitdone/source/browse/trunk/examples/shout_outs.py) and see for yourself.
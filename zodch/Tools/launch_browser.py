
import webbrowser

def launch_browser(url, browser=None):
    """
    A tool that launches a web browser on the user's system.

    :param url: The URL to be opened in the browser. This must be a valid URI.
    :param browser: The browser to use for opening the URL. Valid options are 'chrome', 'firefox', 'safari', 'edge', 'opera'.
                    If not specified, the default browser will be used.
    """
    
    # Map of browser names to the webbrowser.get() method's arguments
    browser_mapping = {
        'chrome': 'google-chrome',
        'firefox': 'firefox',
        'safari': 'safari',
        'edge': 'edge',
        'opera': 'opera'
    }
    
    try:
        if browser and browser.lower() in browser_mapping:
            browser_instance = webbrowser.get(browser_mapping[browser.lower()])
            browser_instance.open(url)
        else:
            # Use default browser
            webbrowser.open(url)
    
    except webbrowser.Error as e:
        print(f"Failed to launch {browser} browser. Error: {e}")

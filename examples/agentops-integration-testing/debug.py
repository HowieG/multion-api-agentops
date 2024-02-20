import multion
multion.login(use_api=True, multion_api_key="08177a120c014ca8887f4962803b21f6", agentops_api_key="e2d78f13-1585-4d45-b482-f67a42ae6099")
multion.set_remote(True)
response = multion.browse(
    {
        "cmd": "what is the weather today in sf",
        "url": "https://www.google.com",
        "maxSteps": 10,
    }
)
# response = multion.create_session({"url": "https://www.google.com", "includeScreenshot": True})
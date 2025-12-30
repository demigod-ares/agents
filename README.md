## Master AI Agentic Engineering -  build autonomous AI Agents

### The not-so-dreaded setup instructions
Perhaps famous last words: but I really, truly hope that I've put together an environment that will be not too horrific to set up!

- Windows people, your instructions are [here](setup/SETUP-PC.md)
- Mac people, yours are [here](setup/SETUP-mac.md)
- Linux people, yours are [here](setup/SETUP-linux.md)

### Important notes for CrewAI week (Week 3)

Windows PC users: you will need to have checked the "gotcha #4" at the top of the [SETUP-PC](setup/SETUP-PC.md) instructions -- installing Microsoft Build Tools.  
If you don't do this, then CrewAI will fail with an obscure error involving Chroma..

Then, you will need to run this command in a Cursor Terminal in the project root directory in order to run the Crew commands:  
`uv tool install crewai`   
And in case you've used Crew before, it might be worth doing this to make sure you have the latest:  
`uv tool upgrade crewai`  

Then please keep in mind for Crew:

1. There are two ways that you can work on the CrewAI project in week 3. Either review the code for each project while I build it, and then do `crewai run` to see it in action. Or if you prefer to be more hands-on, then create your own Crew project from scratch to mirror mine; for example, create `my_debate` to go alongside `debate`, and write the code alongside me. Either approach works!  
2. Windows users: there's a new issue that was recently introduced by one of Crew's libraries. Until this is fixed, you might get a "unicode" error when you try to run `crewai create crew`.  If that happens, please try running this command in the Terminal first: `$env:PYTHONUTF8 = "1"`  
3. Gemini users: in addition to a key in your `.env` file for `GOOGLE_API_KEY`, you will need an identical key for `GEMINI_API_KEY`

### Super useful resources

- The course [resources](https://edwarddonner.com/2025/04/21/the-complete-agentic-ai-engineering-course/) with videos
- Many essential guides in the [guides](guides/01_intro.ipynb) section
- The [troubleshooting](setup/troubleshooting.ipynb) notebook  
- My overall [FAQ](https://edwarddonner.com/faq) page with common issues and questions

### API costs - please read me!

This course does involve making calls to OpenAI and other frontier models, requiring an API key and a small spend, which we set up in the SETUP instructions. If you'd prefer not to spend on API calls, there are cheaper alternatives like DeepSeek and free alternatives like using Ollama!

Details are [here](guides/09_ai_apis_and_ollama.ipynb).

Be sure to monitor your API costs to ensure you are totally happy with any spend. For OpenAI, the dashboard is [here](https://platform.openai.com/usage).
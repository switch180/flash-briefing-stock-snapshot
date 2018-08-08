# Check Stock Price Flash Briefing Skill
This skill allows you to receive a stock quote and potentially a full portfolio update.


## Requirements

1. Robinhood account
1. Amazon account
1. Registration in the amazon developer program - [click here](https://developer.amazon.com/), click on Alexa, and sign up


## TODO

1. Test deploy - need vendoring and need prod_api hack fix for the warmer
1. ASK console instructions
1. easier way to test & generate signature

## Getting started

1. Clone the repo
1. change into the directory
1. setup a pyenv virtualenv with version 3.6.x
1. pip install requirements.txt and requirements-dev.txt
1. vendor the RH and itsdangerous into your vendor folder (see vendor readme)
1. modify chalicelib.config with your portfolio bits
1. test: chalice local  & python -m unittest discover test
1. Generate a signature for your function: generate_signature.py and test the function httpie localhost:8000/(private_method)/{signaure}
1. chalice deploy
1. modify config.json with your prod endpoint for the warmer
1. Create a new flash briefing skill in ASK console
1. Test "alexa, flash briefing"

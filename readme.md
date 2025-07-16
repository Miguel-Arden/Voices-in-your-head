Hello this is another stupid project I've made for some reason. It will simulate what it feels like
to have voices in your head, the voices listen, the voices advise, the voices scream. The voices. The voices.
The voices, they're so loud!

I will now provide a guide on how to setup the 2 services this program needs to run.

Written in Python 3.12.8 (I think)

Before you do anything you must run the following command:
"pip install -r requirements.txt"
This will install all the libaries you need to run this program.

First, we'll make an account on the OpenAI API.

go to (https://auth.openai.com/log-in) and make an account
- Once logged in, click settings at the top right, then click "API keys" on the left side
- Then click the "create new secret key" button
- Your API key will be generated, copy it immediately because you won’t be able to see it again when you close the window.
- Go to your search bar and type the word "env", "Edit the system environment variables" should pop up. Click that, then click "environment variables" Click that and another window should pop up. Click new on "user variables for user" For variable name, set the name to "OPENAI_API_KEY" then add the token you copied into "variable value"

Then we need to add credits to our OpenAI account, to actually be able to use it.

- Click your profile picture on the top right
- Click "Your profile"
- Then click "Billing" on the left side
- Click "Add to credit balance" and then add your payment method and then pay. gpt-4o is a relatively cheap model that works well.
I recommend it for this project.

Now we need to sort Elevenlabs

- Go to https://www.elevenlabs.io.
- Sign up
- After signing up, verify your email (check your inbox).
- Once verified, you'll be redirected to your dashboard.
- In the top right, click your profile icon, then select "Subscription".

You'll get 10k quota for free, which is fine for just normal use, but if you plan on using this
app often for whatever reason, consider anyone of the subscriptions.

Next you need to get your API key.

- While logged in, click your profile icon (top right corner).
- Select “API Key” from the dropdown.
- You’ll be taken to the API Key page:
- If you haven’t generated one yet, click “Generate API Key”.
- Give it any name
- Click “Create”.
- Your key will be shown one time, copy it straight away.
- Store it in your environment variables like last time.

If you did all of this correctly, running this project should now implement voices in your head!
Enjoy!

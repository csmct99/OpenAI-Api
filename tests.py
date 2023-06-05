import debug
from OAI import OpenAI

def TestAll():
    debug.log("Initializing OpenAI API authentication")
    openAI = OpenAI()

    debug.log("Creating chat log")
    openAI.CreateChatLog("default")


    debug.log("Formatting system command ... ")
    systemCommand = openAI.FormatMessage("You are a picky movie critic. You will answer the user's questions with disgust as no movies meet your incredible taste.", "system")

    debug.log("Adding system command to chat log")
    openAI.AddToChatLog(systemCommand, "default")

    debug.log("Formatting user command ... ")
    userCommand = openAI.FormatMessage("What is your favorite movie? I really like toy story! How about you?", "user")

    debug.log("Adding user command to chat log")
    openAI.AddToChatLog(userCommand, "default")

    debug.log("Sending chat log to OpenAI API")
    response = openAI.SendChat(openAI.chatLogs["default"])

    debug.log("Printing response:\n")
    print(response.message.content + "\n")

    openAI.AddToChatLog(response.message, "default")

    debug.log("Formatting user command ... ")
    userCommand = openAI.FormatMessage("Wow! Rude!! Well tell me why you like the movies you like then?", "user")

    debug.log("Adding new user chat to log")
    openAI.AddToChatLog(userCommand, "default")

    debug.log("Sending chat log to OpenAI API")
    response = openAI.SendChat(openAI.chatLogs["default"])

    debug.log("Printing response:\n")
    print(response.message.content + "\n")

    debug.log("Done testing!")

def TestStreams():
    # TODO: Implement
    pass

TestAll()
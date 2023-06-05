import openai
import debug

from debug import DebugLevel
from enums import *


class OpenAI:

    chatLogs = {"default":[]}

    def InitializeAPI(self):
        """
        Initializes the OpenAI API
        """
        debug.log("Initializing OpenAI API authentication", DebugLevel.VERBOSE)
        openai.api_key = self.GetAPIKey()


    def GetAPIKey(self):
        """
        Gets the API key from the api_key.apikey file
        """
        try:
            with open(".apikey", "r") as file:
                apiKey = file.read()
                return apiKey
        except:
            debug.log("API key not found", DebugLevel.ERROR)
            exit()


    def AddToChatLog(self, message, chatLogName = "default"):
        """
        Adds a message to the chat log
        """
        self.chatLogs[chatLogName].append(message)

    def CreateChatLog(self, name):
        """
        Creates a new chat log
        """
        self.chatLogs[name] = []

    def FormatMessage(self, message, role=Roles.USER):
        """
        Formats a message to be sent to the OpenAI API
        """
        return {"role": role, "content": message}



    def SendChat(self, messageHistory, numberOfCompletionOptions = 1, useStream = False):

        response = openai.ChatCompletion.create(
            model = self.engine,
            messages = messageHistory,

            temperature = self.temperature,
            max_tokens = self.max_tokens,
            top_p = self.top_p,
            frequency_penalty = self.frequency_penalty,
            presence_penalty = self.presence_penalty,
            stream = useStream,
            n = numberOfCompletionOptions,
        )

        if useStream:
            return response

        return ChatResponse(response)

    def __init__(self, model= ChatModel.CHATGPT3, temperature= 0.9, max_tokens= 1000, top_p= 1, frequency_penalty= 0, presence_penalty= 0):
        self.InitializeAPI()
        self.engine = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty


class ChatResponse:
    """
    A class to represent a chat response from the OpenAI API
    """

    def __init__(self, response):
        self.id = response["id"]
        self.object = response["object"]
        self.created = response["created"]
        self.model = response["model"]
        self.usage = response["usage"]
        self.choices = response["choices"]

        if self.choices is not None and len(self.choices) > 0:
            self.message = self.choices[0]["message"]
            self.finish_reason = self.choices[0]["finish_reason"]
            self.index = self.choices[0]["index"]
        else:
            self.message = "NO RESPONSE FROM OPENAI"
            self.finish_reason = "UNKNOWN"
            self.index = -1

            debug.log("No response from OpenAI", DebugLevel.ERROR)


# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from botbuilder.schema import ActivityTypes, Attachment, InputHints
from botbuilder.core import TurnContext

from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult
from .prompt_validator_context import PromptValidatorContext

class AttachmentPrompt(Prompt):
    """
    Prompts a user to upload attachments like images.

    By default the prompt will return to the calling dialog a [Attachment]
    """

    # TODO need to define validator PromptValidator type
    def __init__(self, dialog_id: str, validator=None):
        super().__init__(dialog_id, validator)
    
    async def on_prompt(
        self,
        context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
        isRetry: bool
    ):
        if not context:
            raise TypeError('AttachmentPrompt.on_prompt(): context cannot be None.')

        if not isinstance(options, PromptOptions):
            raise TypeError('AttachmentPrompt.on_prompt(): PromptOptions are required for Attachment Prompt dialogs.')
        
        if isRetry and options.retry_prompt:
            options.retry_prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.retry_prompt)
        elif options.prompt:
            options.prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.prompt)
    
    async def on_recognize(
        self,
        context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions
    ) -> PromptRecognizerResult:
        if not context:
            raise TypeError('AttachmentPrompt.on_recognize(): context cannot be None.')
        
        result = PromptRecognizerResult()

        if context.activity.type == ActivityTypes.message:
            message = context.activity
            if isinstance(message.attachments, list) and len(message.attachments) > 0:
                result.succeeded = True
                result.value = message.attachments
        
        return result

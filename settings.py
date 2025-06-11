from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field

class HateDefenderSettings(BaseModel):
    model: str = Field(
        default="IMSyPP/hate_speech_en",
        title="Model",
        description="Insert the model name from Hugging Face Hub for text classification. The model should have a 'HATE' label.",
        extra={"type": "text"}
    )
    
    hate_labels: str = Field(
        default="LABEL_2, LABEL_3",
        title="Hate Labels (comma-separated)",
        description="A comma-separated list of labels from the model that should be considered as hate speech (e.g., HATE, OFFENSIVE). The check is case-insensitive.",
        extra={"type": "TextArea"}
    )
    
    threshold: float = Field(
        default=0.7,
        title="Threshold",
        description="The confidence threshold for hate speech detection (from 0.0 to 1.0). A higher value makes detection stricter.",
        ge=0.0,
        le=1.0
    )
    
    output_message: str = Field(
        default="I can't answer, this message contains hate speech.",
        title="Output Message",
        description="The message sent to the user when hate speech is detected.",
        extra={"type": "textarea"}
    )

@plugin
def settings_model():
    """
    Returns the settings model for the Hate Defender plugin.
    """
    return HateDefenderSettings
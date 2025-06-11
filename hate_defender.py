from cat.mad_hatter.decorators import hook
from transformers import pipeline
from cat.log import log

# Global variables to hold the pipeline and the loaded model name
classifier = None
loaded_model_name = None

@hook(priority=2)
def fast_reply(fast_reply, cat):
    """
    This hook checks user messages for hate speech.
    If hate speech is detected above a configured threshold, it blocks
    the message and returns a predefined response.
    The classification model is loaded once and reused, but it will be
    reloaded if the model name is changed in the settings.
    """
    global classifier, loaded_model_name
    
    settings = cat.mad_hatter.get_plugin().load_settings()
    model_name = settings["model"]
    
    # Load or reload the model if it hasn't been loaded yet
    # or if the model name in settings has changed.
    if classifier is None or loaded_model_name != model_name:
        log.info(f"Loading hate speech detection model: {model_name}")
        try:
            classifier = pipeline("text-classification", model=model_name)
            loaded_model_name = model_name
            log.info(f"Model {model_name} loaded successfully.")
        except Exception as e:
            log.error(f"Failed to load model {model_name}: {e}")
            # Prevent further attempts if the model is invalid
            classifier = None 
            loaded_model_name = None
            return None

    # If the model failed to load in a previous attempt, classifier will be None.
    if classifier is None:
        log.warning("Hate speech classifier is not available. Skipping check.")
        return None

    output_message = settings["output_message"]
    threshold = settings["threshold"]
    
    message = cat.working_memory.user_message_json.text
    
    try:
        result = classifier(message)
    except Exception as e:
        log.error(f"Error during hate speech classification: {e}")
        return None # Let the message pass if classification fails

    # The returned label is converted to uppercase for a case-insensitive comparison
    # with the labels provided in the settings.
    label = result[0]["label"].upper()
    score = result[0]["score"]
    
    # Split the comma-separated string, strip whitespace, and convert to uppercase
    hate_labels_list = settings["hate_labels"].split(',')
    hate_labels = [h.strip().upper() for h in hate_labels_list]

    if label in hate_labels and score > threshold:
        log.info(
            f"Hate speech detected in message: '{message[:50]}...'. "
            f"Label: {label}, Score: {score:.2f} > Threshold: {threshold}. Blocking message."
        )
        output  = {
            "output": output_message
        }
    else:
        log.debug(
            f"Message is not hate speech or below threshold. "
            f"Label: {label}, Score: {score:.2f}, Threshold: {threshold}."
        )
        output = None
    
    return output

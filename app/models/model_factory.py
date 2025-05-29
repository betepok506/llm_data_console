# app/model_factory.py


def get_model_loader(
    use_openai: bool = True,
    api_key=None,
    model_name=None,
    max_tokens: int = 200,
):
    if use_openai:
        from app.models.openai_model import OpenAIModelLoader

        return OpenAIModelLoader(api_key=api_key)
    else:
        from app.models.local_model import LocalModelLoader

        return LocalModelLoader(model_name=model_name)

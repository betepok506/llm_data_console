# app/model_factory.py


def get_model_loader(
    use_openai: bool = True,
    api_key=None,
    model_name=None,
    max_tokens: int = 200,
):
    """
    Фабрика моделей: создаёт нужный загрузчик модели на основе параметров.

    Parameters
    ----------
    use_openai : bool, optional
        Если True, используется модель OpenAI, by default True
    api_key : str, optional
        API-ключ для OpenAI.
    model_name : str, optional
        Название модели.
    max_tokens : int, optional
        Максимальное количество токенов для генерации, by default 200

    Returns
    -------
    ModelInterface
        Экземпляр загрузчика модели.

    Raises
    ------
    NotImplementedError
        Если запрошена модель, отличная от OpenAI.
    """
    if use_openai:
        from app.models.openai_model import OpenAIModelLoader

        return OpenAIModelLoader(api_key=api_key)
    else:
        raise NotImplementedError(
            "Other types of models are not supported at the moment."
        )

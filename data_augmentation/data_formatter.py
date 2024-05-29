USER_PROMPT = (
    f"I will give you batches of contents of articles. For each article, extract all the mentioned cryptocurrencies as a list of strings"
    f"Please structure the answer in json format ready to be loaded by json.loads(). The answer should be a"
    f"list of objects only with fields called content and cryptocurrencies, where cryptocurrencies is the list described previously. For the content field, copy the number of the content only!."
    f"Please do not add any extra characters and make sure it is a list with objects in valid json format!\n"
)

class DataFormatter:
    @classmethod
    def format_data(cls, data_points: list, is_example: bool, start_index: int) -> str:
        text = ""
        for index, data_point in enumerate(data_points):
            if not is_example:
                text += f"Content number {start_index + index }\n"
            text += str(data_point) + "\n"
        return text

    @classmethod
    def format_batch(cls, context_msg: str, data_points: list, start_index: int) -> str:
        delimiter_msg = context_msg
        delimiter_msg += cls.format_data(data_points, False, start_index)
        return delimiter_msg

    @classmethod
    def format_prompt(cls, inference_posts: list, start_index: int):
        initial_prompt = USER_PROMPT
        initial_prompt += f"You must generate exactly a list of {len(inference_posts)} json objects, using the contents provided under CONTENTS FOR GENERATION\n"
        initial_prompt += cls.format_batch(
            "\nCONTENTS FOR GENERATION: \n", inference_posts, start_index
        )
        return initial_prompt
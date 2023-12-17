import os

captcha_images = [
    (
        os.path.join(
            "".join(
                [i + "/" for i in os.path.abspath(__name__).split("\\")[:-2]],
            ),
        ),
        filename.split(".")[0],
    )
    for filename in os.listdir(
        os.path.join(
            "".join(
                [i + "/" for i in os.path.abspath(__name__).split("\\")[:-2]],
            ),
            "docs/captcha",
        )
    )
]
print(captcha_images)

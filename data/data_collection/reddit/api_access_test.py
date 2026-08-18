import requests


URL = "https://www.reddit.com/r/artificial/search.json"

PARAMS = {
    "q": "openai",
    "restrict_sr": "1",
    "sort": "new",
    "limit": 10,
}

HEADERS = {
    "User-Agent": (
        "AI-Evolution-Intelligence/"
        "1.0 by Razny"
    )
}


def main():

    print("=" * 70)
    print("Reddit API Access Test")
    print("=" * 70)

    try:

        response = requests.get(
            URL,
            params=PARAMS,
            headers=HEADERS,
            timeout=30,
        )

        print(
            "HTTP Status:",
            response.status_code
        )

        print(
            "Content-Type:",
            response.headers.get(
                "content-type"
            )
        )

        if response.status_code == 200:

            data = response.json()

            children = (
                data
                .get("data", {})
                .get("children", [])
            )

            print(
                "Posts returned:",
                len(children)
            )

            for item in children[:3]:

                post = item.get(
                    "data",
                    {}
                )

                print("\n---")
                print(
                    "Title:",
                    post.get("title")
                )

                print(
                    "Created:",
                    post.get("created_utc")
                )

                print(
                    "Score:",
                    post.get("score")
                )

        else:

            print(
                "Response:",
                response.text[:500]
            )

    except Exception as error:

        print(
            "ERROR:",
            error
        )


if __name__ == "__main__":
    main()
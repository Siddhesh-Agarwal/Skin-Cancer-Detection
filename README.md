# Skin Cancer Detection

[Live Site](https://skincancerdetection.streamlit.app/)

## Running

1. Install [uv](https://docs.astral.sh/uv/)

1. Install dependencies

    ```bash
    uv install
    ```

1. Add secret `GOOGLE_API_KEY` to the `.streamlit/secrets.toml` file. You can get it from [here](https://console.cloud.google.com/apis/credentials).

1. Run the app

    ```bash
    uv run streamlit run ./Home.py
    ```

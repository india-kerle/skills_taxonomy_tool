mkdir -p ~/.streamlit/
echo “\
[general]\n\
email = \”india.kerle@sciencespo.fr\”\n\
“ > ~/.streamlit/credentials.toml
echo “\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
“ > ~/.streamlit/config.toml
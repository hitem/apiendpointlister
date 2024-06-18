# APIendpointlister

API Endpoint Lister is a Python script designed to fetch and list all API endpoints available in Swagger/OpenAPI JSON files. This tool is useful in conjunction with my other tool [endpointchecker](https://github.com/hitem/endpointchecker), once you got a proper list of swagger/openapi endpoints this tool can help you enumerate all the apiendpoints.

## Features

- Fetches Swagger/OpenAPI JSON from provided URLs.
- Extracts and lists all API endpoints.
- Outputs the results to a specified file.

### Example: 
Input URL file: `http://example.com/swagger/v1/swagger.json` \
~**Script runs, magic 🧙 happens** - **gandalf quotes**~  
Output:\
`http://example.com/api/v1/{userid}/Service/PostUpdate` 
`http://example.com/api/v1/{userid}/Service/PostUpdate/{id}`
`http://example.com/api/v1/{memberid}/Service/Change/Post`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/hitem/apiendpointlister.git
    cd apiendpointlister
    ```
2. Install the required packages:
    ```bash
    pip install requests colorama
    ```
## Usage

Run the script with the required options:
```bash
python3 apiendpointlister.py -h [--help]
python3 apiendpointlister.py -u <path_to_url_list_file> -o <output_file>
```

### Options
- `-u, --urls`: Path to the URL list file (required)
- `-o, --output`: Output file for results (required)

### Example
```bash
python3 apiendpointlister.py -u urllist.txt -o output.txt
```

## Author
- **hitemSec**
- [GitHub](https://github.com/hitem)
- [Mastodon](https://infosec.exchange/@hitem)

## Disclaimer
Use this script with caution. Making numerous requests to external servers may have unintended consequences. Always have permission to test the endpoints you are checking.

---

Feel free to contribute or raise issues on [GitHub](https://github.com/hitem/endpointchecker).

Happy Recon!

import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from urllib3.exceptions import ConnectTimeoutError
import openai

folder_name = "json"
# Function to generate prompts and extract information using GPT-3
def generate_prompt(clean_text):
    prompt = f"Q: Categorise this in a json format:{clean_text}?\nA:"

    try:
        # Call the API using ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=2000,
            temperature=0.8,
            timeout=120
        )

        data = response['choices'][0]['message']['content'].strip()
        return data
    except Exception as e:
            print(f"Error was: {e}")
            skipped_urls.append(scholarship_website_url+str(e))
            return None

# Function to generate prompts and extract scholarship amount using GPT-3
def amount(clean_text):
    prompt = f"Q: Write Amount of scholarship in short from this:{clean_text}?\nA:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.8,
            timeout=120
        )
        data = response['choices'][0]['message']['content'].strip()
        return data
    except Exception as e:
            print(f"Error was: {e}")
            skipped_urls.append(scholarship_website_url+str(e))
            return None

# Function to generate prompts and extract scholarship deadline using GPT-3
def deadline(clean_text):
    prompt = f"Q: Write Deadline of scholarship in short from this:{clean_text}?\nA:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.8,
            timeout=120
        )
        data = response['choices'][0]['message']['content'].strip()
        return data
    except Exception as e:
            print(f"Error was: {e}")
            skipped_urls.append(scholarship_website_url+str(e))
            return None

# Function to generate prompts and extract scholarship eligibility using GPT-3

def eligibility(clean_text):
    prompt = f"Q: Write Eligibility of scholarship in short from this:{clean_text}?\nA:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.8,
            timeout=120
        )
        data = response['choices'][0]['message']['content'].strip()
        return data
    except Exception as e:
            print(f"Error was: {e}")
            skipped_urls.append(scholarship_website_url+str(e))
            return None

# Function to generate prompts and extract scholarship application process using GPT-3

def application_process(clean_text):
    prompt = f"Q: Write the application process of scholarship in short from this:{clean_text}?\nA:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.8,
            timeout=120
        )
        data = response['choices'][0]['message']['content'].strip()
        return data
    except Exception as e:
            print(f"Error was: {e}")
            skipped_urls.append(scholarship_website_url+str(e))
            return None

# Crawl the initial page and extract URLs and scholarship names
url = "https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/school-year/college-freshman"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table", class_="margin-top-twenty-five")
html_contents_list = []

# List to store scholarship website URLs
website_urls = []
skipped_urls = []

# Counter variable for tracking the number of scholarships processed
counter = 0
user_agents = [
    'Mozilla/5.0 (Linux; Android 11; SM-G781B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    # Add more user agents here...
]
# Iterate over the scholarship links within the table
for link in table.find_all("a"):
    scholarship_name = link.text.strip()
    scholarship_url = link["href"]

    if "sortOrder" in scholarship_url:
        continue

    # Search Google for the scholarship website
    search_query = scholarship_name
    for result in search(search_query, tld='com', stop=1, pause=5):
        scholarship_website_url = result
        break

    if scholarship_website_url:
        print(scholarship_website_url)
        website_urls.append(scholarship_website_url)

        if scholarship_website_url.endswith(".pdf") or ".pdf" in scholarship_website_url or "jand" in scholarship_website_url or "hopi" in scholarship_website_url or "capcityaidsfund" in scholarship_website_url or "hsutx" in scholarship_website_url or "bowen" in scholarship_website_url or "txadc" in scholarship_website_url or "lightfoot" in scholarship_website_url or '.jpg' in scholarship_website_url or '.png' in scholarship_website_url or '.doc' in scholarship_website_url or 'docx' in scholarship_website_url:
            print(f"Skipping PDF URL: {scholarship_website_url}")
            skipped_urls.append(scholarship_website_url+"-invalid file extension")
            continue

        try:
             # Use a session to reuse connections and handle cookies
          with requests.Session() as session:
                # Rotate the User-Agent header
            user_agent = random.choice(user_agents)
            headers = {'User-Agent': user_agent}
            response = requests.get(scholarship_website_url,headers=headers, timeout=30)
            if response.status_code == 429:
                print(f"Received 429 error.")
                skipped_urls.append(scholarship_website_url+"-429 error too many requests http")
                time.sleep(10)
                continue
            elif response.status_code == 403:
              print("Error: 403 Forbidden - You don't have permission to access this page.")
              skipped_urls.append(scholarship_website_url+"-403 error forbidden access")
              continue
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                text = soup.get_text()
                clean_text = re.sub(r'\s+', ' ', text).strip()

            # Generate prompts and extract information for the scholarship
                combined_prompt = generate_prompt(clean_text)
                time.sleep(3)
                html=f'''
              <html>
        <body>
            <pre>{combined_prompt}</pre>
            <a href="{scholarship_website_url}">Scholarship Website</a>
        </body>
        </html>
        '''

                file_path = os.path.join(folder_name, scholarship_name + ".html")
                try:
                  with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(html)
                except Exception as e:
                  print(f"An error occurred: {e}")
                  skipped_urls.append(scholarship_website_url+str(e))
                  continue

                amount_val = amount(clean_text)
                time.sleep(3)
                deadline_val = deadline(clean_text)
                time.sleep(3)
                eligibility_val = eligibility(clean_text)
                time.sleep(3)
                application_process_val = application_process(clean_text)
                time.sleep(3)

                if combined_prompt is None:
                   skipped_urls.append(scholarship_website_url)
                   continue

                counter += 1
                print(f"Processed scholarship {counter}/{len(table.find_all('a'))}")

                time.sleep(10)

        except (ConnectTimeoutError, requests.exceptions.RequestException) as e:
            if isinstance(e, ConnectTimeoutError):
                print(f"Connection to {scholarship_website_url} timed out. Skipping...")
                skipped_urls.append(scholarship_website_url+str(e))
                continue
            else:
                print(f"An error occurred while accessing {scholarship_website_url}. Skipping...")
                skipped_urls.append(scholarship_website_url+str(e))
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            skipped_urls.append(scholarship_website_url+str(e))
            continue

        # Append the scholarship information to the HTML content
        html_content = f'''
        <tr>
          <td><a href="{file_path}">{scholarship_name}</a></td>
          <td>{amount_val}</td>
          <td>{deadline_val}</td>
          <td>{eligibility_val}</td>
          <td>{application_process_val}</td>
        </tr>
        '''

        html_contents_list.append(html_content)

# Prepare the final HTML content
html_content = f'''
<html>
<head>
  <title>Scholarship Directory</title>
  <style>
     body {{
      background-color: LightGray;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;

    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }}

    h1 {{
      text-align: center;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th, td {{
      padding: 10px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Scholarship Directory</h1>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Amount</th>
          <th>Deadline</th>
          <th>Eligibility Criteria</th>
          <th>Application process</th>
        </tr>
      </thead>
      <tbody>
        {''.join(html_contents_list)}
      </tbody>
    </table>
  </div>
</body>
</html>
'''

# Write the HTML content to a file
try:
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    print("Output written to output.html")
except Exception as e:
    print(f"An error occurred while writing to the file: {e}")

# Write the skipped URLs to a file
try:
    with open('skipped_websites.txt', 'w', encoding='utf-8') as file:
        for website_url in skipped_urls:
            file.write(website_url + '\n')
    print("Skipped websites written to skipped_websites.txt")
except Exception as e:
    print(f"An error occurred while writing to the file: {e}")

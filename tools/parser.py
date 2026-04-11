import os
import re
import json
from bs4 import BeautifulSoup
import glob

# Detect if we are running from inside the 'tools' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if os.path.basename(os.getcwd()) == 'tools' else os.getcwd()

# Adjust BIBLIO path
biblio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'biblio.json')
BIBLIO = {}
if os.path.exists(biblio_path):
    try:
        with open(biblio_path, 'r', encoding='utf-8') as f:
            BIBLIO = json.load(f)
    except:
        pass

def format_bibtex_to_citation(bibtex_str):
    if not bibtex_str or not bibtex_str.strip(): return None
    def get_field(field, text):
        m = re.search(f"{field}\\s*=\\s*{{([^}}]+)}}", text, re.IGNORECASE)
        if m: return m.group(1).strip()
        m = re.search(f"{field}\\s*=\\s*\"([^\"]+)\"", text, re.IGNORECASE)
        if m: return m.group(1).strip()
        return None
    def format_authors(author_str):
        if not author_str: return "Unknown Author"
        authors = author_str.split(' and ')
        formatted = []
        for a in authors:
            if ',' in a:
                last, first = a.split(',', 1); last = last.strip(); first = first.strip()
                first_initials = " ".join([p[0] + "." for p in first.split() if p])
                formatted.append(f"{first_initials} {last}")
            else:
                parts = a.strip().split()
                if len(parts) > 1:
                    last = parts[-1]; first_initials = " ".join([p[0] + "." for p in parts[:-1] if p])
                    formatted.append(f"{first_initials} {last}")
                else: formatted.append(a.strip())
        if len(formatted) > 2: return ", ".join(formatted[:-1]) + " and " + formatted[-1]
        elif len(formatted) == 2: return f"{formatted[0]} and {formatted[1]}"
        return formatted[0]
    title = get_field("title", bibtex_str)
    authors = format_authors(get_field("author", bibtex_str))
    journal = get_field("journal", bibtex_str) or get_field("booktitle", bibtex_str)
    year = get_field("year", bibtex_str)
    pages = get_field("pages", bibtex_str)
    volume = get_field("volume", bibtex_str)
    if not title: return None
    title = title.replace('{', '').replace('}', '').replace('$', '').replace('\\pi', 'π')
    citation = f"{authors}, \"{title},\" "
    if journal: citation += f"in {journal}, " if "in " not in journal.lower() and "Proc." in journal else f"{journal}, "
    if volume: citation += f"vol. {volume}, "
    if pages: citation += f"pp. {pages}, "
    if year: citation += f"{year}."
    return citation.strip().rstrip(',')

def clean_w3(soup):
    for tag in soup.find_all(True):
        if tag.has_attr('class'):
            tag['class'] = [c for c in tag['class'] if not c.startswith('w3-')]
            if not tag['class']: del tag['class']
    return soup

header_template_top = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>{title} - Alex Robotics</title>
  <meta charset="UTF-8">
  <meta name="author" content="Alexandre Girard, Sherbrooke, Québec, Canada" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <nav class="navbar">
    <div class="container">
      <a href="../index.html" class="nav-brand"><b>Alex</b><span>Robotics</span></a>
      <input type="checkbox" id="nav-toggle" class="nav-toggle-input">
      <label for="nav-toggle" class="nav-toggle-label"><span></span><span></span><span></span></label>
      <ul class="nav-menu">
        <li class="nav-item"><a href="../courses/gro860/">GRO860</a></li>
        <li class="nav-item"><a href="../courses/gmc714/">GMC714</a></li>
        <li class="nav-item"><a href="../material.html">Material</a></li>
        <li class="nav-item"><a href="../projects.html">Portfolio</a></li>
        <li class="nav-item"><a href="../students.html">Students</a></li>
        <li class="nav-item"><a href="../index.html#about">About</a></li>
      </ul>
    </div>
  </nav>
  <header class="hero" id="home" style="height: 35vh; min-height: 250px;">
    <img class="hero-img" src="../img/bg3.jpg" alt="sky">
    <div class="hero-content">
      <h1 style="font-size: 2.5rem; margin-bottom: 0;">{title}</h1>
    </div>
  </header>
  <main>
    <section class="section">
      <div class="container project-container">
        <div class="project-main">
          <div style="margin-bottom: var(--spacing-md);">
            <h2>Abstract</h2>
{abstract}
          </div>
{resources_section}
{media_section}
        </div>
{sidebar_section}
      </div>
    </section>
  </main>
  <footer class="footer">
    <div class="container">
      <p>Alexandre Girard | alex.girard@usherbrooke.ca | <a href="https://www.usherbrooke.ca">UdeS</a> | <a href="https://www.linkedin.com/in/alx87grd">LinkedIn.com/in/alx87grd</a></p>
    </div>
  </footer>
</body>
</html>
"""

def extract_media_from_node(node, grid_items, processed_media):
    if node.name == 'iframe':
        iframe = node
        img = None
    elif node.name == 'img':
        img = node
        iframe = None
    else:
        iframe = node.find('iframe'); img = node.find('img')
        
    if not iframe and not img: return False
    
    fp = ""
    if iframe: fp = iframe.get('src', '')
    elif img: fp = img.get('src', '')
    if not fp or fp in processed_media or 'bg3.jpg' in fp: return False
    processed_media.add(fp)

    # Search for a label in nearby parents
    l_text = ""
    curr = node
    while curr and curr.name not in ['body']:
        label = curr.find('div', class_=re.compile(r'w3-display-topleft'))
        if label: l_text = label.get_text(strip=True); break
        if curr.parent and curr.parent.name in ['div']: curr = curr.parent
        else: break
            
    l_html = f'<div class="card-overlay-title">{l_text}</div>' if l_text else ""
    m_html = ""
    if iframe: 
        iframe['width'] = '100%'; iframe['height'] = '100%'; m_html = str(iframe)
    elif img: 
        src = img.get('src', '').replace('IMG/', 'img/').replace('../IMG/', '../img/')
        m_html = f'<img src="{src}" alt="media" style="width:100%; height:250px; object-fit: cover">'
    
    if m_html:
        grid_items.append(f'<div class="card {"resource-card" if iframe else ""}"><div class="card-img-wrapper">{l_html}{m_html}</div></div>')
        return True
    return False

def extract_links_from_container(container, action_links):
    extracted_year = None
    for a_tag in container.find_all('a'):
        link_text = a_tag.get_text(strip=True); link_href = a_tag.get('href', '#')
        icon = '🔗'; prefix = 'Link: '; t_lower = link_text.lower(); h_lower = link_href.lower()
        is_article = False
        if 'arxiv.org' in h_lower: icon = '📄'; prefix = 'Article (arXiv): '; is_article = True
        elif 'ieeexplore.ieee.org' in h_lower: icon = '📄'; prefix = 'Article (IEEE): '; is_article = True
        elif 'doi.org' in h_lower or 'cdnsciencepub.com' in h_lower: icon = '📄'; prefix = 'Article (Journal): '; is_article = True
        elif 'github.com' in h_lower: icon = '💻'; prefix = 'Code (GitHub): '
        elif 'colab.research' in h_lower: icon = '📓'; prefix = 'Code (Colab): '
        elif 'youtube.com' in h_lower or 'youtu.be' in h_lower: icon = '▶\ufe0f'; prefix = 'Video (YouTube): '
        elif h_lower.endswith('.pdf') or '/pdf/' in h_lower:
            icon = '📋'
            if 'position' in h_lower or 'recruting' in t_lower: prefix = 'Open Role: '
            else: icon = '📄'; prefix = 'Article (PDF): '; is_article = True
        elif h_lower.startswith('mailto:'): icon = '✉\ufe0f'; prefix = 'Contact: '
        elif h_lower.endswith('.html') and not h_lower.startswith('http'): icon = '📁'; prefix = 'Project: '
        
        clean_text = link_text
        if is_article:
            norm_url = link_href.split('#')[0].rstrip('/')
            if norm_url in BIBLIO:
                full_citation = format_bibtex_to_citation(BIBLIO[norm_url])
                if full_citation:
                    clean_text = full_citation
                    year_match = re.search(r'\d{4}', full_citation)
                    if year_match and not extracted_year: extracted_year = year_match.group(0)
            elif clean_text.lower() in ['link', 'here', 'article', 'click here'] or clean_text.startswith('http'):
                clean_text = 'Full Publication'
        else:
            if clean_text.lower() in ['link', 'here', 'article', 'click here'] or clean_text.startswith('http'):
                if 'GitHub' in prefix: clean_text = 'Source Code'
                elif 'Colab' in prefix: clean_text = 'Interactive Notebook'
                elif 'YouTube' in prefix: clean_text = 'Video Demonstration'
                elif 'PDF' in prefix: clean_text = 'PDF Document'
                else: clean_text = 'External Resource'

        for p in ['video:', 'article:', 'code:']:
            if clean_text.lower().startswith(p): clean_text = clean_text[len(p):].strip()
        
        button_html = f'<a href="{link_href}" class="btn-action">{icon} <strong>{prefix.strip()}</strong> {clean_text}</a>'
        action_links.append(button_html)
        p_node = a_tag.parent
        if p_node and p_node.name in ['li', 'p']:
            p_text = p_node.get_text(strip=True)
            if len(p_text) < len(link_text) + 50: p_node.decompose()
            else: a_tag.decompose()
        else: a_tag.decompose()
    return extracted_year

def parse_project(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    title = soup.title.string.strip() if soup.title else "Project"
    abstract_content = ""; grid_items = []; action_links = []; date_param = ""
    meta = {"Client": "", "Team": "", "Keywords": "", "Status": "", "Funding": ""}
    processed_media = set()
    
    text_content = soup.get_text()
    years = re.findall(r'\b(20\d{2})\b', text_content)
    if years:
        years = sorted(list(set(years)))
        date_param = f"{years[0]} - {years[-1]}" if len(years) > 1 else years[0]

    # Find ALL media anywhere in the layout content
    content_area = soup.find('div', class_='w3-content') or soup.find('body')
    for media in content_area.find_all(['img', 'iframe']):
        # Safeguard: hero image
        if 'bg3' in media.get('src', ''): continue
        if extract_media_from_node(media, grid_items, processed_media):
            # Decompose the parent if it's just a wrapper
            parent = media.parent
            if parent and parent.name in ['div', 'p'] and not parent.get_text(strip=True):
                parent.decompose()
            else:
                media.decompose()

    containers = soup.find_all('div', class_='w3-container')
    for c in containers:
        for p in c.find_all('p'):
            pt = p.get_text().strip()
            found = False
            if "Team:" in pt: meta["Team"] = pt.split("Team:", 1)[1].strip(); found = True
            elif "Client:" in pt or "Client/Partner:" in pt:
                meta["Client"] = pt.split("Client:", 1)[1].strip() if "Client:" in pt else pt.split("Partner:", 1)[1].strip(); found = True
            elif "Technical challenges:" in pt or "Challenges:" in pt:
                meta["Keywords"] = pt.split("challenges:", 1)[1].strip() if "challenges:" in pt else pt.split("Challenges:", 1)[1].strip(); found = True
            elif pt.lower().startswith("status:"): meta["Status"] = pt[7:].strip(); found = True
            elif pt.lower().startswith("funding:"): meta["Funding"] = pt[8:].strip(); found = True
            if found: p.decompose()
        
        h1 = c.find('h1')
        if h1: h1.decompose()
        res_year = extract_links_from_container(c, action_links)
        if res_year and not date_param: date_param = res_year
        c = clean_w3(c)
        abstract_content += c.decode_contents().replace('IMG/', 'img/').replace('../IMG/', '../img/').replace('PDF/', 'pdf/').replace('../PDF/', '../pdf/')

    # Cleanup headers & empty tags
    abstract_content = re.sub(r'<(h[34])[^>]*>.*?(article|video|publication|link|source code).*?</\1>', '', abstract_content, flags=re.IGNORECASE | re.DOTALL)
    abstract_content = re.sub(r'<(h[123456])[^>]*>\s*</\1>', '', abstract_content)
    abstract_content = re.sub(r'<(p|div|ul)[^>]*>\s*</\1>', '', abstract_content)
    for old, new in [('personnal', 'personal'), ('mecanical', 'mechanical'), ('recruting', 'recruiting'), ('mecanics', 'mechanics'), ('developping', 'developing'), ('ressources', 'resources'), ('indepedent', 'independent')]:
        abstract_content = abstract_content.replace(old, new)

    sidebar_items = ""
    for k in ["Client", "Team"]:
        if meta[k]: sidebar_items += f'<div class="project-meta-item"><div class="project-meta-label">{k}</div><div class="project-meta-value">{meta[k]}</div></div>'
    if date_param: sidebar_items += f'<div class="project-meta-item"><div class="project-meta-label">Date</div><div class="project-meta-value">{date_param}</div></div>'
    for k in ["Status", "Funding", "Keywords"]:
        if meta[k]: sidebar_items += f'<div class="project-meta-item"><div class="project-meta-label">{k}</div><div class="project-meta-value">{meta[k]}</div></div>'
    
    sidebar_section = f'<div class="project-sidebar"><h3>Project Details</h3>{sidebar_items}</div>' if sidebar_items else ""
    resources_section = f'<div style="margin-bottom: var(--spacing-md);"><h3>Publications & Resources</h3><div class="action-links-row" style="flex-direction: column; align-items: flex-start;">{"".join(action_links)}</div></div>' if action_links else ""
    media_section = f'<div style="margin-bottom: var(--spacing-md);"><h3 style="margin-bottom: var(--spacing-sm);">Project Media</h3><div class="grid">{"".join(grid_items)}</div></div>' if grid_items else ""

    out_html = header_template_top.format(title=title, abstract=abstract_content.strip(), resources_section=resources_section, media_section=media_section, sidebar_section=sidebar_section)
    with open(file_path, 'w', encoding='utf-8') as f: f.write(out_html)

# Update the main execution loop
proj_glob = os.path.join(BASE_DIR, 'projects/*.html')
for pf in glob.glob(proj_glob):
    if "project_template.html" not in pf:
        parse_project(pf)
print("Parsing complete.")

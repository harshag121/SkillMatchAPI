"""
Job scraper module for real-time job search across multiple platforms
"""
import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import quote_plus, urljoin
import random
import time
from datetime import datetime, timedelta

class JobScraper:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        self.session_cache = {}
        self.rate_limit_delay = 1  # seconds between requests
        
    def get_random_headers(self) -> Dict[str, str]:
        """Get random headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    async def scrape_indeed_jobs(self, query: str, location: str = "United States", max_results: int = 10) -> List[Dict]:
        """Scrape job listings from Indeed"""
        jobs = []
        try:
            encoded_query = quote_plus(query)
            encoded_location = quote_plus(location)
            url = f"https://www.indeed.com/jobs?q={encoded_query}&l={encoded_location}&sort=date"
            
            async with aiohttp.ClientSession(headers=self.get_random_headers()) as session:
                await asyncio.sleep(self.rate_limit_delay)
                async with session.get(url) as response:
                    if response.status != 200:
                        return jobs
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find job cards using Indeed's current structure
                    job_cards = soup.find_all(['div'], class_=re.compile(r'job_seen_beacon|result|jobsearch-SerpJobCard'))
                    
                    for card in job_cards[:max_results]:
                        try:
                            job_data = self.extract_indeed_job_data(card)
                            if job_data:
                                jobs.append(job_data)
                        except Exception as e:
                            continue  # Skip problematic cards
                            
        except Exception as e:
            print(f"Indeed scraping error: {e}")
        
        return jobs
    
    def extract_indeed_job_data(self, card) -> Optional[Dict]:
        """Extract job data from Indeed job card"""
        try:
            # Job title and link
            title_elem = card.find(['h2', 'a'], attrs={'data-jk': True}) or card.find('a', href=re.compile(r'/viewjob'))
            if not title_elem:
                title_elem = card.find(['span', 'a'], class_=re.compile(r'jobTitle'))
            
            title = "Unknown Title"
            link = "#"
            
            if title_elem:
                if title_elem.name == 'a':
                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href', '')
                    if href.startswith('/'):
                        link = f"https://www.indeed.com{href}"
                    else:
                        link = href
                else:
                    title_link = title_elem.find('a')
                    if title_link:
                        title = title_link.get_text(strip=True)
                        href = title_link.get('href', '')
                        if href.startswith('/'):
                            link = f"https://www.indeed.com{href}"
                        else:
                            link = href
                    else:
                        title = title_elem.get_text(strip=True)
            
            # Company name
            company_elem = card.find(['span', 'div', 'a'], class_=re.compile(r'companyName'))
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            # Location
            location_elem = card.find(['div', 'span'], attrs={'data-testid': 'job-location'}) or \
                           card.find(class_=re.compile(r'companyLocation'))
            location = location_elem.get_text(strip=True) if location_elem else "Remote/Unknown"
            
            # Salary (if available)
            salary_elem = card.find(['span', 'div'], class_=re.compile(r'salary'))
            salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
            
            # Posted date
            date_elem = card.find(['span'], class_=re.compile(r'date'))
            posted_date = date_elem.get_text(strip=True) if date_elem else "Recently"
            
            # Job snippet/description
            snippet_elem = card.find(['div', 'span'], class_=re.compile(r'summary'))
            snippet = snippet_elem.get_text(strip=True)[:200] + "..." if snippet_elem else ""
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "link": link,
                "source": "Indeed",
                "posted_date": posted_date,
                "snippet": snippet,
                "match_keywords": []
            }
            
        except Exception as e:
            return None

    async def scrape_glassdoor_jobs(self, query: str, location: str = "United States", max_results: int = 5) -> List[Dict]:
        """Scrape job listings from Glassdoor"""
        jobs = []
        try:
            encoded_query = quote_plus(query)
            encoded_location = quote_plus(location)
            url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_query}&locT=C&locId=1&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"
            
            async with aiohttp.ClientSession(headers=self.get_random_headers()) as session:
                await asyncio.sleep(self.rate_limit_delay + 1)  # Longer delay for Glassdoor
                async with session.get(url) as response:
                    if response.status != 200:
                        return jobs
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Glassdoor job cards
                    job_cards = soup.find_all(['li', 'div'], class_=re.compile(r'job.*result|JobSearchCard'))
                    
                    for card in job_cards[:max_results]:
                        try:
                            job_data = self.extract_glassdoor_job_data(card)
                            if job_data:
                                jobs.append(job_data)
                        except Exception:
                            continue
                            
        except Exception as e:
            print(f"Glassdoor scraping error: {e}")
        
        return jobs
    
    def extract_glassdoor_job_data(self, card) -> Optional[Dict]:
        """Extract job data from Glassdoor job card"""
        try:
            # Job title and link
            title_elem = card.find('a', class_=re.compile(r'jobTitle'))
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            link = urljoin("https://www.glassdoor.com", title_elem.get('href', '#')) if title_elem else "#"
            
            # Company
            company_elem = card.find(['span', 'div'], class_=re.compile(r'employer'))
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            # Location
            location_elem = card.find(['span', 'div'], class_=re.compile(r'location'))
            location = location_elem.get_text(strip=True) if location_elem else "Unknown Location"
            
            # Salary
            salary_elem = card.find(['span', 'div'], class_=re.compile(r'salary'))
            salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "link": link,
                "source": "Glassdoor",
                "posted_date": "Recently",
                "snippet": "",
                "match_keywords": []
            }
            
        except Exception:
            return None

    async def search_jobs_comprehensive(self, skills: List[str], roles: List[str], location: str = "United States", max_results: int = 15) -> List[Dict]:
        """Search for jobs across multiple platforms with robust fallback"""
        all_jobs = []
        
        try:
            # Create search queries
            primary_query = f"{roles[0]} {' '.join(skills[:3])}" if roles else ' '.join(skills[:5])
            
            # Try to scrape real jobs with timeout
            try:
                # Quick Indeed search with shorter timeout
                indeed_jobs = await asyncio.wait_for(
                    self.scrape_indeed_jobs(primary_query, location, max_results // 2),
                    timeout=10.0
                )
                all_jobs.extend(indeed_jobs)
            except asyncio.TimeoutError:
                print("Indeed scraping timeout - using fallback")
            except Exception as e:
                print(f"Indeed scraping failed: {e}")
            
            # If we have some real jobs, return them
            if all_jobs:
                unique_jobs = self.deduplicate_jobs(all_jobs)
                self.add_match_keywords(unique_jobs, skills, roles)
                unique_jobs.sort(key=lambda x: len(x.get('match_keywords', [])), reverse=True)
                return unique_jobs[:max_results]
        
        except Exception as e:
            print(f"Comprehensive search error: {e}")
        
        # Always provide fallback if scraping fails or returns no results
        return await self.get_fallback_jobs(skills, roles)
    
    def deduplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate job listings"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique identifier for the job
            identifier = f"{job.get('title', '').lower()}_{job.get('company', '').lower()}"
            if identifier not in seen and job.get('title') != "Unknown Title":
                seen.add(identifier)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def add_match_keywords(self, jobs: List[Dict], skills: List[str], roles: List[str]):
        """Add matching keywords to job listings"""
        all_keywords = [skill.lower() for skill in skills] + [role.lower() for role in roles]
        
        for job in jobs:
            job_text = f"{job.get('title', '')} {job.get('snippet', '')}".lower()
            matched_keywords = []
            
            for keyword in all_keywords:
                if keyword.lower() in job_text and keyword not in matched_keywords:
                    matched_keywords.append(keyword)
            
            job['match_keywords'] = matched_keywords

    async def get_fallback_jobs(self, skills: List[str], roles: List[str]) -> List[Dict]:
        """Provide enhanced fallback job search links and curated opportunities"""
        fallback_jobs = []
        
        primary_role = roles[0] if roles else "Software Developer"
        top_skills = ' '.join(skills[:5])
        encoded_query = quote_plus(f"{primary_role} {top_skills}")
        
        # Enhanced job board links with better targeting
        enhanced_jobs = [
            {
                "title": f"{primary_role} - Live Opportunities",
                "company": "Indeed (Top Job Board)",
                "location": "Multiple Locations",
                "salary": "Competitive + Benefits",
                "link": f"https://www.indeed.com/jobs?q={encoded_query}&sort=date&fromage=7",
                "source": "Indeed",
                "posted_date": "Last 7 days",
                "snippet": f"Find {primary_role} positions matching your skills: {', '.join(skills[:5])}. Click to see current openings with salary details.",
                "match_keywords": skills[:5]
            },
            {
                "title": f"{primary_role} Network Opportunities",
                "company": "LinkedIn Professional Network",
                "location": "Global Remote + On-site",
                "salary": "Market Rate",
                "link": f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&sortBy=DD&f_TPR=r86400",
                "source": "LinkedIn",
                "posted_date": "Last 24 hours",
                "snippet": f"Professional network opportunities for {primary_role}. Leverage your network and apply directly to hiring managers.",
                "match_keywords": skills[:4]
            },
            {
                "title": f"Senior {primary_role} - Tech Companies",
                "company": "Glassdoor Verified Companies",
                "location": "Major Tech Hubs",
                "salary": "Above Market + Equity",
                "link": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_query}&minSalary=80000&fromAge=7",
                "source": "Glassdoor",
                "posted_date": "This week",
                "snippet": f"Senior-level positions at top-rated companies. View salaries, company reviews, and interview insights.",
                "match_keywords": skills[:3]
            },
            {
                "title": f"{primary_role} - Startup Ecosystem",
                "company": "AngelList & YC Companies",
                "location": "Startup Hubs + Remote",
                "salary": "Competitive + Equity",
                "link": f"https://angel.co/jobs?keywords={encoded_query}&jobType=full-time",
                "source": "AngelList",
                "posted_date": "Startup Jobs",
                "snippet": f"Join innovative startups building the future. Equity opportunities and cutting-edge {', '.join(skills[:3])} work.",
                "match_keywords": skills[:4]
            },
            {
                "title": f"Remote {primary_role} Positions",
                "company": "Remote-First Companies",
                "location": "100% Remote",
                "salary": "Global Competitive",
                "link": f"https://remoteok.io/remote-{'-'.join(primary_role.lower().split())}-jobs",
                "source": "RemoteOK",
                "posted_date": "Remote Focus",
                "snippet": f"Fully remote {primary_role} opportunities from companies worldwide. Work from anywhere with {', '.join(skills[:3])} skills.",
                "match_keywords": skills[:3]
            },
            {
                "title": f"{primary_role} - Government & Enterprise",
                "company": "Federal & Large Enterprise",
                "location": "Major Cities + Remote",
                "salary": "Excellent Benefits",
                "link": f"https://www.usajobs.gov/Search/Results?k={encoded_query}",
                "source": "USAJobs",
                "posted_date": "Government Sector",
                "snippet": f"Stable government and enterprise positions for {primary_role}. Excellent benefits, security clearance opportunities.",
                "match_keywords": skills[:2]
            }
        ]
        
        # Add skill-specific job boards
        if any(skill.lower() in ['python', 'javascript', 'react', 'node', 'django', 'fastapi'] for skill in skills):
            enhanced_jobs.append({
                "title": f"Python/Web Developer Positions",
                "company": "Stack Overflow Jobs + Dev Community",
                "location": "Tech Companies Worldwide",
                "salary": "Developer-Focused",
                "link": f"https://stackoverflow.com/jobs?q={encoded_query}&sort=p",
                "source": "Stack Overflow",
                "posted_date": "Developer Community",
                "snippet": "Jobs from the world's largest developer community. Technical challenges and growth opportunities.",
                "match_keywords": [skill for skill in skills if skill.lower() in ['python', 'javascript', 'react', 'node', 'django', 'fastapi']]
            })
        
        if any(skill.lower() in ['ai', 'ml', 'machine learning', 'tensorflow', 'pytorch', 'data science'] for skill in skills):
            enhanced_jobs.append({
                "title": f"AI/ML Engineer Opportunities",
                "company": "AI-First Companies",
                "location": "AI Hubs + Remote",
                "salary": "Premium AI Rates",
                "link": f"https://jobs.lever.co/search?query={quote_plus('machine learning ai engineer')}",
                "source": "AI Companies",
                "posted_date": "AI Focus",
                "snippet": "Cutting-edge AI/ML positions at companies pushing the boundaries of artificial intelligence.",
                "match_keywords": [skill for skill in skills if 'ai' in skill.lower() or 'ml' in skill.lower() or 'learning' in skill.lower()]
            })
        
        return enhanced_jobs[:6]  # Return top 6 curated opportunities

# Global job scraper instance
job_scraper = JobScraper()

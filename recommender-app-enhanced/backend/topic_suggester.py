import requests
import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# You can replace this with your actual YouTube API key
API_KEY = "AIzaSyBlXXCEvOf_ok-UJL77sMdV9yJ5lrch8_Q"

class RegionalTopicSuggester:
    """Regional Topic Suggestion System for Content Creators"""

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.region_codes = {
            'India': 'IN', 'United States': 'US', 'United Kingdom': 'GB', 'Canada': 'CA',
            'Australia': 'AU', 'Germany': 'DE', 'France': 'FR', 'Japan': 'JP',
            'South Korea': 'KR', 'Brazil': 'BR', 'Mexico': 'MX', 'Singapore': 'SG',
            'UAE': 'AE', 'Thailand': 'TH', 'Philippines': 'PH', 'Indonesia': 'ID',
            'Vietnam': 'VN', 'Malaysia': 'MY', 'Pakistan': 'PK', 'Bangladesh': 'BD'
        }

    def get_mock_trending_data(self, region_code, max_results=25):
        """Generate mock trending data for demonstration purposes"""
        mock_topics = [
            {
                "title": "Breaking: Latest Tech Innovation Shaking the Industry",
                "description": "Revolutionary technology breakthrough announced today...",
                "channel": "TechNews Today",
                "views": 2500000,
                "likes": 125000,
                "comments": 8500,
                "published": datetime.now().isoformat(),
                "tags": ["technology", "innovation", "breakthrough"],
                "category": "Technology"
            },
            {
                "title": "Viral Dance Challenge Taking Over Social Media",
                "description": "New dance trend spreading rapidly across platforms...",
                "channel": "Entertainment Central",
                "views": 8500000,
                "likes": 450000,
                "comments": 25000,
                "published": (datetime.now() - timedelta(days=1)).isoformat(),
                "tags": ["dance", "viral", "challenge"],
                "category": "Entertainment"
            },
            {
                "title": "Ultimate Study Tips for Better Learning",
                "description": "Science-backed methods to improve study efficiency...",
                "channel": "EduMaster",
                "views": 1200000,
                "likes": 85000,
                "comments": 5200,
                "published": (datetime.now() - timedelta(days=2)).isoformat(),
                "tags": ["education", "study", "learning"],
                "category": "Education"
            },
            {
                "title": "Championship Finals: Incredible Sports Moments",
                "description": "Unforgettable highlights from the championship game...",
                "channel": "Sports Zone",
                "views": 5500000,
                "likes": 275000,
                "comments": 18000,
                "published": (datetime.now() - timedelta(days=1)).isoformat(),
                "tags": ["sports", "championship", "highlights"],
                "category": "Sports"
            },
            {
                "title": "Gaming World Record Broken Live on Stream",
                "description": "Speedrunner achieves impossible world record...",
                "channel": "Gaming Pro",
                "views": 3200000,
                "likes": 180000,
                "comments": 12000,
                "published": datetime.now().isoformat(),
                "tags": ["gaming", "world record", "speedrun"],
                "category": "Gaming"
            }
        ]

        # Add region-specific content
        if region_code == 'IN':
            mock_topics.extend([
                {
                    "title": "Bollywood Star's Secret Wedding Revealed",
                    "description": "Celebrity couple's private ceremony details...",
                    "channel": "Bollywood Insider",
                    "views": 4500000,
                    "likes": 225000,
                    "comments": 15000,
                    "published": datetime.now().isoformat(),
                    "tags": ["bollywood", "celebrity", "wedding"],
                    "category": "Entertainment"
                }
            ])
        elif region_code == 'US':
            mock_topics.extend([
                {
                    "title": "Hollywood Awards Night Shocking Moments",
                    "description": "Unexpected events at this year's award ceremony...",
                    "channel": "Hollywood Tonight",
                    "views": 6200000,
                    "likes": 310000,
                    "comments": 22000,
                    "published": datetime.now().isoformat(),
                    "tags": ["hollywood", "awards", "celebrities"],
                    "category": "Entertainment"
                }
            ])

        return pd.DataFrame(mock_topics)

    def fetch_regional_trends(self, region_code, max_results=25):
        """Fetch trending topics (uses mock data for demo)"""
        logger.info(f"Fetching trends for region: {region_code}")

        try:
            # For demo purposes, use mock data
            # In production, replace with actual YouTube API calls
            df = self.get_mock_trending_data(region_code, max_results)

            if not df.empty:
                df = df.head(max_results)
                logger.info(f"Found {len(df)} trending topics")

            return df

        except Exception as e:
            logger.error(f"Error fetching trends: {e}")
            return pd.DataFrame()

    def _categorize_content(self, title, description):
        """Automatically categorize content based on keywords"""
        text = (title + " " + description).lower()

        category_keywords = {
            "Technology": ["tech", "ai", "software", "app", "digital", "innovation"],
            "Entertainment": ["movie", "show", "celebrity", "entertainment", "funny", "comedy"],
            "Education": ["learn", "tutorial", "guide", "how to", "education", "tips"],
            "Sports": ["sports", "game", "match", "football", "cricket", "player"],
            "Music": ["music", "song", "album", "artist", "concert", "singer"],
            "Gaming": ["gaming", "game", "gameplay", "streamer", "esports"],
            "Lifestyle": ["lifestyle", "vlog", "daily", "life", "personal"],
            "Health": ["health", "fitness", "workout", "diet", "wellness"],
            "Business": ["business", "money", "finance", "investment", "startup"],
            "Travel": ["travel", "trip", "vacation", "destination", "adventure"]
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        return "General"

    def extract_trending_keywords(self, df):
        """Extract trending keywords from titles and descriptions"""
        if df.empty:
            return []

        all_text = " ".join(df['title'].fillna("") + " " + df['description'].fillna("")).lower()

        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'a', 'an', 'this', 'that', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'video', 'youtube', 'watch', 'subscribe', 'like', 'comment', 'share',
            'new', 'latest', 'best', 'top', 'how', 'what', 'why', '2025'
        }

        words = [word for word in all_text.split() 
                if len(word) > 3 and word not in stop_words and word.isalpha()]
        word_freq = Counter(words)

        return word_freq.most_common(12)

    def generate_topic_suggestions(self, trending_df, region_name, user_interests=None, count=8):
        """Generate personalized content topic suggestions"""
        logger.info(f"Generating {count} suggestions for {region_name}")

        if trending_df.empty:
            return []

        suggestions = []

        # Extract trending keywords
        trending_keywords = self.extract_trending_keywords(trending_df)

        # Generate suggestions based on trending topics
        for i, (_, row) in enumerate(trending_df.head(count).iterrows()):
            keywords = self._extract_keywords_from_title(row['title'])

            suggestion = {
                'id': i + 1,
                'title': self._create_engaging_title(keywords, row['category'], region_name),
                'description': self._generate_description(keywords, row['category']),
                'category': row['category'],
                'keywords': keywords[:4],
                'content_angles': self._generate_content_angles(keywords, row['category']),
                'trending_factor': self._calculate_trending_factor(row),
                'estimated_views': self._estimate_potential_views(row),
                'difficulty': self._assess_creation_difficulty(row['category']),
                'monetization_potential': self._assess_monetization(row['category']),
                'original_trend': row['title'][:100]
            }
            suggestions.append(suggestion)

        # Sort by trending factor
        suggestions.sort(key=lambda x: x['trending_factor'], reverse=True)

        return suggestions

    def _extract_keywords_from_title(self, title):
        """Extract meaningful keywords from title"""
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        words = [word for word in title.split() if word.lower() not in stop_words and len(word) > 2]
        return words[:5]

    def _create_engaging_title(self, keywords, category, region):
        """Create engaging titles for content creators"""
        if not keywords:
            return f"Trending {category} Content in {region}"

        main_concept = " ".join(keywords[:2]).title()

        templates = [
            f"The Truth About {main_concept} That {region} Needs to Know",
            f"Why {main_concept} is Dominating {region} Right Now",
            f"Ultimate {main_concept} Guide - {region} Edition",
            f"How {main_concept} is Changing Everything in {region}",
            f"{main_concept} Secrets: What {region} Creators Are Doing"
        ]

        return templates[hash(main_concept) % len(templates)]

    def _generate_description(self, keywords, category):
        """Generate compelling descriptions for suggestions"""
        concept = " ".join(keywords[:2]).title() if keywords else category

        descriptions = [
            f"Explore the latest trends in {concept} and discover what's capturing audiences worldwide.",
            f"Deep dive into {concept} with expert insights and practical tips for content creators.",
            f"Uncover the secrets behind successful {concept} content and boost your engagement.",
            f"Master {concept} creation with proven strategies and trending techniques.",
            f"Everything you need to know about {concept} to stay ahead of the competition."
        ]

        return descriptions[hash(concept) % len(descriptions)]

    def _generate_content_angles(self, keywords, category):
        """Generate different content approach angles"""
        concept = " ".join(keywords[:2]).title() if keywords else category

        angles = [
            f"Beginner's complete guide to {concept}",
            f"Advanced {concept} techniques and strategies",
            f"Common {concept} mistakes and how to avoid them",
            f"{concept} trends and future predictions",
            f"Behind-the-scenes of successful {concept} creators"
        ]

        return angles

    def _calculate_trending_factor(self, row):
        """Calculate trending factor (0-100)"""
        views = row.get('views', 0)
        likes = row.get('likes', 0)
        comments = row.get('comments', 0)

        # Base score from views
        if views > 5000000:
            score = 90
        elif views > 2000000:
            score = 75
        elif views > 1000000:
            score = 60
        elif views > 500000:
            score = 45
        else:
            score = 30

        # Boost from engagement
        if views > 0:
            engagement_rate = (likes + comments) / views
            score += min(10, engagement_rate * 10000)

        return min(100, int(score))

    def _estimate_potential_views(self, row):
        """Estimate potential views for user content"""
        original_views = row.get('views', 0)
        return int(original_views * 0.05)  # 5% of original trend

    def _assess_creation_difficulty(self, category):
        """Assess content creation difficulty"""
        difficulty_map = {
            "Technology": "Medium",
            "Entertainment": "Easy",
            "Education": "Medium",
            "Sports": "Easy",
            "Gaming": "Easy",
            "Music": "Medium",
            "Lifestyle": "Easy",
            "Business": "Hard",
            "Travel": "Medium"
        }
        return difficulty_map.get(category, "Medium")

    def _assess_monetization(self, category):
        """Assess monetization potential"""
        monetization_map = {
            "Technology": "High",
            "Entertainment": "Medium",
            "Education": "High",
            "Sports": "Medium",
            "Gaming": "High",
            "Music": "Medium",
            "Lifestyle": "High",
            "Business": "High",
            "Travel": "Medium"
        }
        return monetization_map.get(category, "Medium")

def get_regional_suggestions(region_name, user_interests=None):
    """Main function to get topic suggestions"""
    suggester = RegionalTopicSuggester()

    # Get region code
    region_code = suggester.region_codes.get(region_name, 'US')

    # Fetch trending data
    trending_df = suggester.fetch_regional_trends(region_code)

    if trending_df.empty:
        return {
            'suggestions': [],
            'trending_keywords': [],
            'statistics': {
                'total_trends': 0,
                'categories': {},
                'region': region_name
            }
        }

    # Generate suggestions
    suggestions = suggester.generate_topic_suggestions(trending_df, region_name, user_interests)

    # Extract trending keywords
    keywords = suggester.extract_trending_keywords(trending_df)

    # Generate statistics
    categories = trending_df['category'].value_counts().to_dict()

    statistics = {
        'total_trends': len(trending_df),
        'categories': categories,
        'region': region_name,
        'avg_views': int(trending_df['views'].mean()) if 'views' in trending_df.columns else 0,
        'top_keywords': [{'keyword': k, 'count': c} for k, c in keywords[:10]]
    }

    return {
        'suggestions': suggestions,
        'trending_keywords': keywords,
        'statistics': statistics
    }

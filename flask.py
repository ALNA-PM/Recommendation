import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from sklearn.neighbors import KDTree
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from pybloom_live import BloomFilter
from datetime import datetime, timedelta
import json

# -------------------------
# Configuration Constants
# -------------------------
API_KEY = "AIzaSyBlXXCEvOf_ok-UJL77sMdV9yJ5lrch8_Q"
MAX_RESULTS = 20
N_PSEUDO_USERS = 50

# -------------------------
# 1. Enhanced User Profile System
# -------------------------
class UserProfileSystem:
    """
    Comprehensive user profiling system that builds user preferences
    based on various data sources and provides personalized recommendations
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.content_categories = [
            "Film & Animation", "Autos & Vehicles", "Music", "Pets & Animals", 
            "Sports", "Travel & Events", "Gaming", "People & Blogs", "Comedy", 
            "Entertainment", "News & Politics", "Howto & Style", "Education", 
            "Science & Technology"
        ]
        
    def create_user_profile(self, user_id, demographics=None, explicit_preferences=None):
        """Create a comprehensive user profile with multiple data sources"""
        profile = {
            'user_id': user_id,
            'demographics': demographics or {},
            'explicit_preferences': explicit_preferences or {},
            'viewing_history': [],
            'implicit_feedback': {
                'watch_time': {},
                'likes': [],
                'shares': [],
                'searches': [],
                'skip_patterns': {}
            },
            'content_preferences': {cat: 0.0 for cat in self.content_categories},
            'temporal_patterns': {
                'active_hours': [],
                'preferred_duration': 'medium',
                'weekend_vs_weekday': {'weekend': 0.5, 'weekday': 0.5}
            },
            'profile_updated': datetime.now()
        }
        
        # Initialize content preferences from explicit preferences
        if explicit_preferences:
            for category, score in explicit_preferences.items():
                if category in profile['content_preferences']:
                    profile['content_preferences'][category] = score
        
        self.user_profiles[user_id] = profile
        return profile
    
    def update_implicit_feedback(self, user_id, video_data, interaction_type, value):
        """Update user profile based on implicit feedback"""
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        
        if interaction_type == 'watch_time':
            video_id = video_data['id']
            watch_duration = value
            video_duration = video_data.get('duration', 300)  # default 5 minutes
            
            # Calculate completion rate
            completion_rate = min(watch_duration / video_duration, 1.0)
            profile['implicit_feedback']['watch_time'][video_id] = {
                'duration': watch_duration,
                'completion_rate': completion_rate,
                'timestamp': datetime.now()
            }
            
            # Update category preferences based on completion rate
            category = video_data.get('category', 'Entertainment')
            if category in profile['content_preferences']:
                current_pref = profile['content_preferences'][category]
                profile['content_preferences'][category] = current_pref + (completion_rate * 0.1)
        
        elif interaction_type == 'like':
            profile['implicit_feedback']['likes'].append({
                'video_id': video_data['id'],
                'category': video_data.get('category', 'Entertainment'),
                'timestamp': datetime.now()
            })
            
            # Boost category preference for liked videos
            category = video_data.get('category', 'Entertainment')
            if category in profile['content_preferences']:
                profile['content_preferences'][category] += 0.15
        
        elif interaction_type == 'search':
            profile['implicit_feedback']['searches'].append({
                'query': value,
                'timestamp': datetime.now()
            })
        
        elif interaction_type == 'skip':
            # Track skip patterns to understand dislikes
            category = video_data.get('category', 'Entertainment')
            skip_time = value
            video_duration = video_data.get('duration', 300)
            
            if category not in profile['implicit_feedback']['skip_patterns']:
                profile['implicit_feedback']['skip_patterns'][category] = []
            
            profile['implicit_feedback']['skip_patterns'][category].append({
                'skip_ratio': skip_time / video_duration,
                'timestamp': datetime.now()
            })
            
            # Decrease preference for frequently skipped categories
            if len(profile['implicit_feedback']['skip_patterns'][category]) > 3:
                avg_skip_ratio = np.mean([s['skip_ratio'] for s in 
                                        profile['implicit_feedback']['skip_patterns'][category][-5:]])
                if avg_skip_ratio < 0.3:  # Skipping early indicates dislike
                    profile['content_preferences'][category] -= 0.05
    
    def get_user_preference_vector(self, user_id):
        """Get a comprehensive preference vector for the user"""
        if user_id not in self.user_profiles:
            return np.ones(len(self.content_categories)) / len(self.content_categories)
        
        profile = self.user_profiles[user_id]
        prefs = np.array(list(profile['content_preferences'].values()))
        
        # Normalize preferences
        if np.sum(prefs) > 0:
            prefs = prefs / np.sum(prefs)
        else:
            prefs = np.ones(len(self.content_categories)) / len(self.content_categories)
        
        return prefs
    
    def calculate_user_similarity(self, user1_id, user2_id):
        """Calculate similarity between two users based on their profiles"""
        if user1_id not in self.user_profiles or user2_id not in self.user_profiles:
            return 0.0
        
        profile1 = self.user_profiles[user1_id]
        profile2 = self.user_profiles[user2_id]
        
        # Content preference similarity
        prefs1 = np.array(list(profile1['content_preferences'].values()))
        prefs2 = np.array(list(profile2['content_preferences'].values()))
        
        content_sim = cosine_similarity([prefs1], [prefs2])[0][0]
        
        # Demographic similarity
        demo_sim = 0.0
        demo1 = profile1['demographics']
        demo2 = profile2['demographics']
        
        if demo1 and demo2:
            common_features = set(demo1.keys()) & set(demo2.keys())
            if common_features:
                matches = sum(1 for key in common_features if demo1[key] == demo2[key])
                demo_sim = matches / len(common_features)
        
        # Combine similarities
        overall_similarity = 0.7 * content_sim + 0.3 * demo_sim
        return overall_similarity

# -------------------------
# 2. Enhanced Video Fetching with User Preferences
# -------------------------
def collect_user_credentials():
    """Collect user information for personalized recommendations"""
    print("🔍 Let's create your personalized profile!")
    print("Please provide the following information:")
    
    demographics = {}
    demographics['approx. age of audiance'] = int(input("Enter your age: "))
    demographics['education'] = input("Enter your education level (School/Graduate/Postgraduate): ")
    demographics['language'] = input("Enter your preferred language: ")
    
    print("\nContent Preferences (rate 0-10, 0=not interested, 10=very interested):")
    explicit_preferences = {}
    categories = [
        "Film & Animation", "Autos & Vehicles", "Music", "Pets & Animals", 
        "Sports", "Travel & Events", "Gaming", "People & Blogs", "Comedy", 
        "Entertainment", "News & Politics", "Howto & Style", "Education", 
        "Science & Technology"
    ]
    
    for category in categories:
        try:
            score = float(input(f"{category}: ")) / 10.0  # Normalize to 0-1
            if 0 <= score <= 1:
                explicit_preferences[category] = score
        except:
            explicit_preferences[category] = 0.1  # Default low interest
    
    return demographics, explicit_preferences

def build_personalized_search_queries(user_profile, language_preference="தமிழ்"):
    """Build search queries based on user preferences"""
    content_prefs = user_profile['content_preferences']
    
    # Get top 3 preferred categories
    top_categories = sorted(content_prefs.items(), key=lambda x: x[1], reverse=True)[:3]
    
    queries = []
    base_terms = {
        "Film & Animation": ["movie", "film", "animation", "trailer"],
        "Music": ["song", "music", "album", "concert"],
        "Sports": ["sports", "cricket", "football", "match"],
        "Entertainment": ["entertainment", "celebrity", "show"],
        "Education": ["tutorial", "learn", "education", "class"],
        "Science & Technology": ["tech", "technology", "science", "gadget"],
        "Comedy": ["comedy", "funny", "humor", "joke"],
        "Gaming": ["gaming", "game", "gameplay", "esports"],
        "News & Politics": ["news", "politics", "current affairs"],
        "Travel & Events": ["travel", "event", "festival", "place"],
        "Howto & Style": ["howto", "tutorial", "style", "tips"],
        "Autos & Vehicles": ["car", "bike", "vehicle", "auto"],
        "Pets & Animals": ["pet", "animal", "dog", "cat"],
        "People & Blogs": ["vlog", "blog", "lifestyle"]
    }
    
    # Build queries for top categories
    for category, score in top_categories:
        if score > 0.1 and category in base_terms:
            terms = base_terms[category]
            for term in terms[:2]:  # Use top 2 terms per category
                queries.append(f"{language_preference} {term}")
    
    # Add general query
    queries.append(language_preference)
    
    return queries[:5]  # Limit to 5 queries

def fetch_personalized_videos(api_key, user_profile, max_results=20):
    """Fetch videos based on user preferences"""
    queries = build_personalized_search_queries(user_profile)
    all_videos = []
    
    for query in queries:
        try:
            # Search for videos
            search_url = "https://www.googleapis.com/youtube/v3/search"
            search_params = {
                "part": "snippet",
                "type": "video",
                "regionCode": "IN",
                "maxResults": max_results // len(queries),
                "q": query,
                "key": api_key
            }
            
            resp = requests.get(search_url, params=search_params)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            
            video_ids = [item["id"]["videoId"] for item in items]
            
            if video_ids:
                # Get detailed video information
                stats_url = "https://www.googleapis.com/youtube/v3/videos"
                stats_params = {
                    "part": "snippet,statistics,contentDetails",
                    "id": ",".join(video_ids),
                    "key": api_key
                }
                
                resp = requests.get(stats_url, params=stats_params)
                resp.raise_for_status()
                detailed_items = resp.json().get("items", [])
                
                for item in detailed_items:
                    snip = item["snippet"]
                    stats = item["statistics"]
                    
                    # Categorize video (simple heuristic)
                    title_lower = snip.get("title", "").lower()
                    description_lower = snip.get("description", "").lower()
                    category = categorize_video(title_lower, description_lower)
                    
                    video_data = {
                        "id": item["id"],
                        "title": snip.get("title", ""),
                        "description": snip.get("description", ""),
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                        "category": category,
                        "query_used": query
                    }
                    all_videos.append(video_data)
        
        except Exception as e:
            print(f"Error fetching videos for query '{query}': {e}")
            continue
    
    return pd.DataFrame(all_videos).drop_duplicates(subset=['id']).head(max_results)

def categorize_video(title, description):
    """Simple video categorization based on keywords"""
    category_keywords = {
        "Music": ["song", "music", "album", "singer", "melody"],
        "Sports": ["cricket", "football", "sports", "match", "game"],
        "Education": ["learn", "tutorial", "education", "teaching", "class"],
        "Entertainment": ["movie", "film", "actor", "actress", "entertainment"],
        "Science & Technology": ["tech", "technology", "science", "gadget", "innovation"],
        "Comedy": ["comedy", "funny", "humor", "laugh", "joke"],
        "Gaming": ["gaming", "game", "gameplay", "player"],
        "News & Politics": ["news", "politics", "government", "election"],
        "Travel & Events": ["travel", "trip", "place", "event", "festival"],
    }
    
    text = title + " " + description
    
    for category, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return "Entertainment"  # Default category

# -------------------------
# 3. Enhanced Recommendation System
# -------------------------
def build_personalized_embeddings(df, user_profile):
    """Build text embeddings with user preference weighting"""
    texts = (df["title"] + " " + df["description"]).fillna("")
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    X_tfidf = tfidf.fit_transform(texts)
    
    svd = TruncatedSVD(n_components=50, random_state=0)
    embeddings = svd.fit_transform(X_tfidf)
    
    # Weight embeddings by user category preferences
    user_prefs = user_profile['content_preferences']
    for i, category in enumerate(df['category']):
        if category in user_prefs:
            pref_weight = 1.0 + user_prefs[category]  # Boost preferred categories
            embeddings[i] *= pref_weight
    
    return embeddings, tfidf, svd

def personalized_hybrid_recommend(df, user_profile, embeddings, target_idx, top_n=10):
    """Generate personalized recommendations using hybrid approach"""
    user_prefs = user_profile['content_preferences']
    n_items = len(df)
    
    if target_idx >= n_items:
        target_idx = 0
    
    tgt_emb = embeddings[target_idx]
    
    # Calculate various scores
    content_scores = []
    category_scores = []
    demographic_scores = []
    popularity_scores = df["views"].values.astype(float)
    popularity_scores = (popularity_scores - popularity_scores.min()) / (popularity_scores.ptp() + 1e-9)
    
    user_age = user_profile['demographics'].get('age', 25)
    user_education = user_profile['demographics'].get('education', 'Graduate')
    
    for idx in range(n_items):
        if idx == target_idx:
            content_scores.append(0)
            category_scores.append(0)
            demographic_scores.append(0)
            continue
        
        # Content similarity
        content_sim = cosine_similarity([tgt_emb], [embeddings[idx]])[0][0]
        content_scores.append(max(0, content_sim))
        
        # Category preference score
        video_category = df.iloc[idx]['category']
        category_score = user_prefs.get(video_category, 0.1)
        category_scores.append(category_score)
        
        # Demographic boost
        demo_score = 1.0
        if video_category == 'Gaming' and user_age < 30:
            demo_score = 1.2
        elif video_category == 'News & Politics' and user_age > 35:
            demo_score = 1.2
        elif video_category == 'Education' and user_education in ['Graduate', 'Postgraduate']:
            demo_score = 1.15
        demographic_scores.append(demo_score)
    
    content_scores = np.array(content_scores)
    category_scores = np.array(category_scores)
    demographic_scores = np.array(demographic_scores)
    
    # Weighted combination
    final_scores = (
        0.25 * content_scores +
        0.45 * category_scores +
        0.20 * popularity_scores +
        0.10 * demographic_scores
    )
    
    # Build recommendation list
    candidates = []
    for i, score in enumerate(final_scores):
        if i == target_idx:
            continue
        
        candidates.append({
            "idx": i,
            "id": df.iloc[i]["id"],
            "title": df.iloc[i]["title"],
            "category": df.iloc[i]["category"],
            "views": int(df.iloc[i]["views"]),
            "final_score": score,
            "content_sim": content_scores[i],
            "category_score": category_scores[i],
            "popularity_score": popularity_scores[i],
            "demographic_boost": demographic_scores[i]
        })
    
    # Sort and return top N
    top_candidates = sorted(candidates, key=lambda x: x["final_score"], reverse=True)[:top_n]
    return top_candidates

def track_user_interaction(user_system, user_id, video_data, interaction_type, value):
    """Track user interactions for profile learning"""
    user_system.update_implicit_feedback(user_id, video_data, interaction_type, value)
    print(f"✅ Tracked {interaction_type} for {user_id}")

# -------------------------
# 4. Main Enhanced System
# -------------------------
def main():
    print("🎯 Enhanced Personalized Video Recommendation System")
    print("=" * 60)
    
    # Initialize user profile system
    user_system = UserProfileSystem()
    
    # Get user credentials and preferences
    print("\n📝 Step 1: Creating your personalized profile...")
    demographics, explicit_preferences = collect_user_credentials()
    
    user_id = f"user_{hash(str(demographics) + str(explicit_preferences)) % 10000}"
    user_profile = user_system.create_user_profile(user_id, demographics, explicit_preferences)
    
    print(f"✅ Created profile for user: {user_id}")
    print(f"📊 Top preferences: {dict(sorted(explicit_preferences.items(), key=lambda x: x[1], reverse=True)[:3])}")
    
    # Fetch personalized videos
    print("\n🔍 Step 2: Fetching personalized videos based on your interests...")
    try:
        df = fetch_personalized_videos(API_KEY, user_profile, max_results=MAX_RESULTS)
        if df.empty:
            print("❌ No personalized videos found. Using fallback...")
            # Fallback to original method if needed
            df = fetch_trending_videos(API_KEY, MAX_RESULTS)
    except Exception as e:
        print(f"⚠️ Error fetching personalized videos: {e}")
        print("Using trending videos as fallback...")
        df = fetch_trending_videos(API_KEY, MAX_RESULTS)
    
    if df.empty:
        print("❌ No videos fetched. Please check your API key and internet connection.")
        return
    
    print(f"✅ Fetched {len(df)} personalized videos")
    
    # Build personalized embeddings
    embeddings, tfidf, svd = build_personalized_embeddings(df, user_profile)
    
    # Show available videos
    print(f"\n📺 Available videos (personalized for your interests):")
    for idx, row in df.iterrows():
        print(f"{idx}: {row['title']} (Category: {row['category']}, Views: {row['views']:,})")
    
    # Get user choice
    try:
        choice = int(input(f"\nEnter video index (0-{len(df)-1}) for recommendations: "))
        if choice < 0 or choice >= len(df):
            print("Invalid index. Using first video.")
            choice = 0
    except:
        print("Invalid input. Using first video.")
        choice = 0
    
    target_video = df.iloc[choice]
    print(f"\n🎯 Target video: [{choice}] {target_video['title']}")
    print(f"   Category: {target_video['category']} | Views: {target_video['views']:,}")
    
    # Generate personalized recommendations
    print(f"\n🔮 Generating personalized recommendations...")
    recommendations = personalized_hybrid_recommend(
        df, user_profile, embeddings, choice, top_n=10
    )
    
    print(f"\n⭐ Top 10 Personalized Recommendations for You:")
    print("=" * 70)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']}")
        print(f"    Category: {rec['category']} | Views: {rec['views']:,}")
        print(f"    Score: {rec['final_score']:.3f} | Content: {rec['content_sim']:.3f} | "
              f"Category: {rec['category_score']:.3f} | Popularity: {rec['popularity_score']:.3f}")
        print()
    
    # Simulate some user interactions
    print("🔄 Simulating user interactions to improve future recommendations...")
    for i, rec in enumerate(recommendations[:3]):  # Simulate interaction with top 3
        video_data = {
            'id': rec['id'],
            'title': rec['title'],
            'category': rec['category'],
            'duration': 300  # 5 minutes average
        }
        
        # Simulate different interactions
        if i == 0:  # First video - user likes it
            track_user_interaction(user_system, user_id, video_data, 'like', True)
            track_user_interaction(user_system, user_id, video_data, 'watch_time', 280)  # Watched most of it
        elif i == 1:  # Second video - user watches partially
            track_user_interaction(user_system, user_id, video_data, 'watch_time', 150)  # Watched half
        else:  # Third video - user skips early
            track_user_interaction(user_system, user_id, video_data, 'skip', 30)  # Skipped after 30 seconds
    
    # Show updated preferences
    updated_prefs = user_system.user_profiles[user_id]['content_preferences']
    print(f"\n📈 Updated preferences after interactions:")
    top_updated_prefs = dict(sorted(updated_prefs.items(), key=lambda x: x[1], reverse=True)[:5])
    for category, score in top_updated_prefs.items():
        print(f"   {category}: {score:.3f}")
    
    print(f"\n✨ System learned from your interactions and will provide better recommendations next time!")
    print("=" * 70)
    print("🎉 Enhanced personalization features:")
    print("  ✅ User profile creation with demographics & preferences")
    print("  ✅ Personalized video fetching based on interests")
    print("  ✅ Hybrid recommendation scoring")
    print("  ✅ Real-time learning from user interactions")
    print("  ✅ Category-aware preference modeling")
    print("  ✅ Demographic-based content filtering")

# Original fetch_trending_videos function for fallback
def fetch_trending_videos(api_key, max_results=20):
    """Fallback function to fetch trending videos"""
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "type": "video",
        "regionCode": "IN",
        "maxResults": max_results,
        "q": "தமிழ்",
        "key": api_key
    }
    
    try:
        resp = requests.get(search_url, params=search_params)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        
        video_ids = [item["id"]["videoId"] for item in items]
        
        if video_ids:
            stats_url = "https://www.googleapis.com/youtube/v3/videos"
            stats_params = {
                "part": "snippet,statistics",
                "id": ",".join(video_ids),
                "key": api_key
            }
            resp = requests.get(stats_url, params=stats_params)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            
            videos = []
            for item in items:
                snip = item["snippet"]
                stats = item["statistics"]
                videos.append({
                    "id": item["id"],
                    "title": snip.get("title", ""),
                    "description": snip.get("description", ""),
                    "views": int(stats.get("viewCount", 0)),
                    "category": "Entertainment"  # Default category
                })
            
            return pd.DataFrame(videos)
    except Exception as e:
        print(f"Error in fallback function: {e}")
    
    return pd.DataFrame()

if __name__ == "__main__":
    main()
import React, { useState } from "react";
import axios from "axios";
import {
  FaFilm, FaCar, FaMusic, FaDog, FaFutbol, FaPlane, FaGamepad,
  FaUser, FaLaugh, FaTv, FaNewspaper, FaWrench, FaBook, FaMicroscope
} from "react-icons/fa";

const genres = [
  { name: "Film & Animation", icon: <FaFilm /> },
  { name: "Autos & Vehicles", icon: <FaCar /> },
  { name: "Music", icon: <FaMusic /> },
  { name: "Pets & Animals", icon: <FaDog /> },
  { name: "Sports", icon: <FaFutbol /> },
  { name: "Travel & Events", icon: <FaPlane /> },
  { name: "Gaming", icon: <FaGamepad /> },
  { name: "People & Blogs", icon: <FaUser /> },
  { name: "Comedy", icon: <FaLaugh /> },
  { name: "Entertainment", icon: <FaTv /> },
  { name: "News & Politics", icon: <FaNewspaper /> },
  { name: "How to & Style", icon: <FaWrench /> },
  { name: "Education", icon: <FaBook /> },
  { name: "Science & Technology", icon: <FaMicroscope /> },
];

// Entertainment hierarchical options
const entertainmentSubgenres = [
  {
    name: "Movies & TV",
    subs: [
      "Movie Reviews & Reactions",
      "Behind the Scenes",
      "Trailers & Teasers",
      "Celebrity Interviews",
      "Film Analysis / Breakdown"
    ],
  },
  {
    name: "Music & Performance",
    subs: [
      "Music Videos",
      "Live Performances",
      "Instrument Tutorials",
      "Cover Songs",
      "Dance Performances",
      "Lyrics Explained"
    ],
  },
  {
    name: "Gaming & Esports",
    subs: [
      "Gameplay Walkthroughs",
      "Live Streams",
      "Game Reviews",
      "Esports Tournaments",
      "Game Storylines / Lore"
    ],
  },
  {
    name: "Comedy & Humor",
    subs: [
      "Sketches & Skits",
      "Stand-up Comedy",
      "Pranks",
      "Funny Reactions / Memes",
      "Satire & Parody"
    ],
  },
  {
    name: "Pop Culture & Celebrities",
    subs: [
      "Gossip & News",
      "Red Carpet Events",
      "Influencer Content",
      "Fan Theories"
    ],
  },
  {
    name: "Lifestyle & Vlogs",
    subs: [
      "Daily Vlogs",
      "Challenges",
      "Couple / Family Channels",
      "Unboxing & Reactions",
      "Behind-the-scenes of Influencers"
    ],
  },
  {
    name: "Fictional & Storytelling",
    subs: [
      "Short Films",
      "Audio Dramas",
      "Animation Series",
      "Web Series",
      "Story-based Podcasts"
    ],
  }
];

// Education hierarchical options
const educationSubgenres = [
  {
    name: "Academic Learning",
    subs: [
      "Mathematics (Algebra, Geometry, Calculus, Statistics)",
      "Science (Physics, Chemistry, Biology, Environmental Science)",
      "Computer Science & Programming (Python, AI/ML, Web Dev, Cybersecurity)",
      "History & Civics",
      "Geography",
      "Language Learning (English, Spanish, French, etc.)",
      "Economics & Commerce"
    ],
  },
  {
    name: "Skill Development",
    subs: [
      "Communication Skills",
      "Public Speaking",
      "Writing & Grammar",
      "Leadership & Management",
      "Critical Thinking",
      "Problem Solving",
      "Emotional Intelligence (EQ)"
    ],
  },
  {
    name: "Career & Professional Growth",
    subs: [
      "Resume Building / Interview Prep",
      "Job & Internship Tips",
      "Career Advice (Tech, Business, Design)",
      "Certification Courses (AWS, Azure, Google Cloud, Databricks, etc.)",
      "Productivity & Time Management"
    ],
  },
  {
    name: "Higher Education & Research",
    subs: [
      "College Reviews & Study Abroad",
      "Research Tutorials (Papers, Thesis, Data Analysis)",
      "Online Courses / MOOCs (Coursera, Udemy)",
      "EdTech Tools & Platforms"
    ],
  },
  {
    name: "Educational Entertainment (\"Edutainment\")",
    subs: [
      "Science Experiments",
      "Animated Learning",
      "Fun Facts & Trivia",
      "Simplified Concepts (e.g., \"Physics in Real Life\")",
      "History / Science Explained Videos"
    ],
  },
  {
    name: "Motivation & Self-Improvement",
    subs: [
      "Study Motivation",
      "Habit Building",
      "Mindset & Focus",
      "Inspirational Stories of Learners"
    ],
  }
];

export default function GenreSelector({ username, onInterestsSet }) {
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [entertainmentSelected, setEntertainmentSelected] = useState([]);
  const [entertainmentSubSelected, setEntertainmentSubSelected] = useState({});
  const [educationSelected, setEducationSelected] = useState([]);
  const [educationSubSelected, setEducationSubSelected] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Genre multi-select
  const selectGenre = (genre) => {
    setSelectedGenres(prev =>
      prev.includes(genre)
        ? prev.filter(g => g !== genre)
        : [...prev, genre]
    );
    setMessage("");
  };

  // Entertainment subgenre multi-select
  const toggleEntertainment = (subGenre) => {
    setEntertainmentSelected(prev =>
      prev.includes(subGenre)
        ? prev.filter(s => s !== subGenre)
        : [...prev, subGenre]
    );
  };

  // Entertainment sub-sub-genre multi-select
  const toggleEntertainmentSub = (parent, subSubGenre) => {
    setEntertainmentSubSelected(prev => {
      const arr = prev[parent] || [];
      const updated = arr.includes(subSubGenre)
        ? arr.filter(s => s !== subSubGenre)
        : [...arr, subSubGenre];
      return { ...prev, [parent]: updated };
    });
  };

  // Education subgenre multi-select
  const toggleEducation = (subGenre) => {
    setEducationSelected(prev =>
      prev.includes(subGenre)
        ? prev.filter(s => s !== subGenre)
        : [...prev, subGenre]
    );
  };

  // Education sub-sub-genre multi-select
  const toggleEducationSub = (parent, subSubGenre) => {
    setEducationSubSelected(prev => {
      const arr = prev[parent] || [];
      const updated = arr.includes(subSubGenre)
        ? arr.filter(s => s !== subSubGenre)
        : [...arr, subSubGenre];
      return { ...prev, [parent]: updated };
    });
  };

  // Submit interests
  const handleSubmit = async () => {
    if (selectedGenres.length === 0) {
      setMessage("Please select at least one genre.");
      return;
    }
    setIsLoading(true);
    setMessage("");

    // Collect all selections
    const interests = {
      genres: selectedGenres,
      entertainment: {
        selected: entertainmentSelected,
        subSelected: entertainmentSubSelected
      },
      education: {
        selected: educationSelected,
        subSelected: educationSubSelected
      },
    };

    try {
      const response = await axios.post("http://localhost:5000/set_interests", {
        username,
        interests,
      });
      if (response.data.success) {
        console.log("✅ Interests saved successfully");
        onInterestsSet(selectedGenres, interests);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || "Failed to save interests. Please try again.";
      setMessage(errorMessage);
      console.error("❌ Failed to save interests:", errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate total selections
  const getTotalSelections = () => {
    let total = selectedGenres.length;
    total += entertainmentSelected.length;
    total += educationSelected.length;
    total += Object.values(entertainmentSubSelected).flat().length;
    total += Object.values(educationSubSelected).flat().length;
    return total;
  };

  return (
    <div className="genre-selector-container">
      <h2>Choose Your Content Interests</h2>
      <p style={{ textAlign: 'center', marginBottom: '25px', color: '#666' }}>
        Select the genres you're interested in creating content for:
      </p>

      <div className="genre-list">
        {genres.map(genre => (
          <div
            key={genre.name}
            className={`genre-item ${selectedGenres.includes(genre.name) ? "selected" : ""}`}
            onClick={() => selectGenre(genre.name)}
          >
            {genre.icon}
            <span>{genre.name}</span>
          </div>
        ))}
      </div>

      {/* Show Entertainment subgenres/sub-sub-genres for selection */}
      {selectedGenres.includes("Entertainment") && (
        <div className="subgenre-section">
          <h3>🎭 Entertainment Subgenres</h3>
          {entertainmentSubgenres.map(sub => (
            <div key={sub.name} className="subgenre-item">
              <label>
                <input
                  type="checkbox"
                  checked={entertainmentSelected.includes(sub.name)}
                  onChange={() => toggleEntertainment(sub.name)}
                /> {sub.name}
              </label>
              <div className="subsub-list">
                {sub.subs.map(subSub =>
                  <label key={subSub}>
                    <input
                      type="checkbox"
                      checked={entertainmentSubSelected[sub.name]?.includes(subSub) || false}
                      onChange={() => toggleEntertainmentSub(sub.name, subSub)}
                    /> {subSub}
                  </label>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Show Education subgenres/sub-sub-genres for selection */}
      {selectedGenres.includes("Education") && (
        <div className="subgenre-section">
          <h3>🎓 Education Subgenres</h3>
          {educationSubgenres.map(sub => (
            <div key={sub.name} className="subgenre-item">
              <label>
                <input
                  type="checkbox"
                  checked={educationSelected.includes(sub.name)}
                  onChange={() => toggleEducation(sub.name)}
                /> {sub.name}
              </label>
              <div className="subsub-list">
                {sub.subs.map(subSub =>
                  <label key={subSub}>
                    <input
                      type="checkbox"
                      checked={educationSubSelected[sub.name]?.includes(subSub) || false}
                      onChange={() => toggleEducationSub(sub.name, subSub)}
                    /> {subSub}
                  </label>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: '25px' }}>
        <button
          onClick={handleSubmit}
          disabled={isLoading || selectedGenres.length === 0}
        >
          {isLoading ? "Saving..." : "Continue"}
        </button>

        {message && (
          <div className={message.includes("Please select") ? "error" : "success"}>
            {message}
          </div>
        )}
      </div>

      {getTotalSelections() > 0 && (
        <div className="selection-summary">
          Total selections: {getTotalSelections()} 
          {selectedGenres.length > 0 && ` (${selectedGenres.length} main genres)`}
          {entertainmentSelected.length > 0 && ` + ${entertainmentSelected.length} entertainment categories`}
          {educationSelected.length > 0 && ` + ${educationSelected.length} education categories`}
        </div>
      )}
    </div>
  );
}

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Groq from "groq-sdk";
import "./OnboardingInterests.css";

const groq = new Groq({
  apiKey: process.env.REACT_APP_GROQ_API_KEY,
  dangerouslyAllowBrowser: true,
});

const interestSchema = {
  type: "object",
  properties: {
    interests: {
      type: "array",
      items: { type: "string" },
      title: "Interests",
    },
  },
  required: ["interests"],
  title: "InterestList",
};

const defaultInterests = [
  "Hiking",
  "Cooking",
  "Photography",
  "Book Club",
  "Gaming",
  "Movie Nights",
  "Board Games",
  "Fitness",
  "Volunteering",
  "Travel",
];

const OnBoardingInterests = ({ updateUserData }) => {
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [suggestedInterests, setSuggestedInterests] =
    useState(defaultInterests);
  const [newInterest, setNewInterest] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const getGroqChatCompletion = async () => {
      try {
        const jsonSchema = JSON.stringify(interestSchema, null, 2);
        const completion = await groq.chat.completions.create({
          messages: [
            {
              role: "system",
              content: `You are an assistant that suggests activities to do with other people. Output interests in JSON format.\nThe JSON object must use the schema: ${jsonSchema}`,
            },
            {
              role: "user",
              content:
                "Suggest 10 interests for activities to do with other people.",
            },
          ],
          model: "llama3-8b-8192",
          temperature: 0.5,
          max_tokens: 150,
          top_p: 1,
          response_format: { type: "json_object" },
        });

        const content = JSON.parse(completion.choices[0].message.content);
        if (content.interests && Array.isArray(content.interests)) {
          setSuggestedInterests(content.interests);
        } else {
          throw new Error("Invalid response format");
        }
      } catch (err) {
        console.error("Failed to fetch suggestions", err);
        // Use default interests if API call fails
        setSuggestedInterests(defaultInterests);
      }
    };

    getGroqChatCompletion();
  }, []);

  const toggleInterest = (interestName) => {
    setSelectedInterests((prev) =>
      prev.includes(interestName)
        ? prev.filter((i) => i !== interestName)
        : [...prev, interestName],
    );
  };

  const addInterest = () => {
    if (
      newInterest &&
      !selectedInterests.includes(newInterest) &&
      !suggestedInterests.includes(newInterest)
    ) {
      setSelectedInterests([...selectedInterests, newInterest]);
      setSuggestedInterests([...suggestedInterests, newInterest]);
      setNewInterest("");
    }
  };

  const handleNext = () => {
    updateUserData("interests", selectedInterests);
    navigate("/calendar");
  };

  return (
    <div className="onboarding-profile">
      <a href="/" className="logo-link">
        <div className="logo">FreeTime</div>
      </a>
      <form onSubmit={(e) => e.preventDefault()}>
        <div className="form-group">
          <label>What do you like to do with others?</label>
          <div className="interests-grid">
            {suggestedInterests.map((interest, index) => (
              <div
                key={index}
                className={`interest-item ${selectedInterests.includes(interest) ? "selected" : ""}`}
                onClick={() => toggleInterest(interest)}
              >
                <span className="interest-name">{interest}</span>
              </div>
            ))}
          </div>
          <br />
          <div className="add-interest-container">
            <input
              type="text"
              value={newInterest}
              onChange={(e) => setNewInterest(e.target.value)}
              placeholder="Add new interest"
            />
            <br /> <br />
            <button className="add-button" type="button" onClick={addInterest}>
              Add
            </button>
          </div>
        </div>
        <button className="next-button" type="button" onClick={handleNext}>
          Next
        </button>
      </form>
    </div>
  );
};

export default OnBoardingInterests;

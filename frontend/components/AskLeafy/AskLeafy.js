"use client";

import { useState } from "react";
import styles from "./askLeafy.module.css";

const AskLeafy = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAsk = async () => {

    setLoading(true);

    console.log("Asking Leafy:", question);
    // Use proxy route instead of direct backend URL
    const apiUrl = "/api/askTheLlm";

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Answer:", data);
      setAnswer(data.result);
      setDocs(data.similar_docs);
    } catch (error) {
      console.error("Error:", error);
    }
    finally {
      setLoading(false); // Reset loading state
    }
  };

  console.log(docs.length > 0 ? JSON.stringify(docs[0].metadata) : "");

  const handleSuggestionOne = () => {
    setQuestion(
      "Summarise claims involving accidental car failures"
    );
  };

  const handleSuggestionTwo = () => {
    setQuestion(
      "For adverse weather related claims, what is the average loss amount?"
    );
  };

  return (
    <div className={styles.content}>
      <div className={styles.chat}>
        <h2>Ask Leafy a Question</h2>
        <div className={styles.question}>
          <input
            className={styles.input}
            type="text"
            value={question}
            onChange={handleChange}
            placeholder="Type your question here..."
          />
           <button
            className={styles.askBtn}
            onClick={handleAsk}
            disabled={loading} // Disable button while loading
          >
            {loading ? <div className={styles.spinner}></div> : "Ask"}
          </button>
          <div className={styles.suggestedQuestions}>
            <p>Suggested Questions:</p>

            <button className={styles.suggestion} onClick={handleSuggestionOne}>
              Summarise claims involving accidental car failures
            </button>
            <button className={styles.suggestion} onClick={handleSuggestionTwo}>
              For adverse weather related claims, what is the average loss
              amount?
            </button>
          </div>
        </div>
        <div>{answer && <p className={styles.answer}>{answer}</p>}</div>
      </div>
      <div className={styles.references}>
        <h2>References</h2>

        {docs.length > 0 && (
          <div>
            {docs.map((doc, index) => (
              <div className={styles.referenceCards} key={index}>
                <div className={styles.imgSection}>
                  <img
                    src={`/photos/${doc.metadata.photo}`}
                    alt="Claim photo"
                  />
                </div>

                <div className={styles.contentSection}>
                  <div className={styles.upperSection}>
                    <div className={styles.fieldWrapper}>
                      <p className={styles.fieldTitle}>Customer ID:</p>
                      <p className={styles.fieldContent}>
                        {doc.metadata.customerID}
                      </p>
                    </div>

                    <div className={styles.fieldWrapper}>
                      <p className={styles.fieldTitle}>Claim Date:</p>
                      <p className={styles.fieldContent}>
                        {doc.metadata.claimFNOLDate}
                      </p>
                    </div>

                    <div className={styles.fieldWrapper}>
                      <p className={styles.fieldTitle}>Loss Amount:</p>
                      <p className={styles.lossAmount}>
                        ${doc.metadata.totalLossAmount}
                      </p>
                    </div>
                  </div>

                  <div className={styles.lowerSection}>
                    <p className={styles.fieldTitle}>Claim Description:</p>
                    <p className={styles.fieldContent}>{doc.page_content}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AskLeafy;

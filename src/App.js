import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
    const [topic, setTopic] = useState('');
    const [faqs, setFaqs] = useState('');

    const generateFaq = async () => {
        const response = await axios.post('http://localhost:5000/generate_faq', { topic });
        setFaqs(response.data);
    };

    return (
        <div>
            <h1>FAQ Generator</h1>
            <input
                type="text"
                placeholder="Enter topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
            />
            <button onClick={generateFaq}>Generate FAQs</button>
            <pre>{faqs}</pre>
        </div>
    );
};

export default App;

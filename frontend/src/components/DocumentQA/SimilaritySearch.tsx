import React from 'react';

interface SimilaritySearchProps {
  context: string[];
}

const SimilaritySearch: React.FC<SimilaritySearchProps> = ({ context }) => {
  return (
    <div className="similarity-search">
      <h3>Document Similarity Search</h3>
      {context.map((doc, idx) => (
        <div key={idx} className="similarity-item">
          <p>{doc}</p>
          <hr />
        </div>
      ))}
    </div>
  );
};

export default SimilaritySearch;

import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  type?: 'button' | 'submit';
  className?: string;
}

const Button: React.FC<ButtonProps> = ({ label, onClick, type = 'button', className }) => {
  return (
    <button type={type} className={`btn ${className}`} onClick={onClick}>
      {label}
    </button>
  );
};

export default Button;

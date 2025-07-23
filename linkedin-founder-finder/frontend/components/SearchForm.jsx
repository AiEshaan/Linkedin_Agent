import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';

const SearchForm = ({ onSearch, isLoading }) => {
  const [formData, setFormData] = useState({
    domain: '',
    location: '',
    role: 'Founder',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div className="grid gap-2">
          <Label htmlFor="domain">Domain/Industry</Label>
          <Input
            id="domain"
            name="domain"
            placeholder="e.g., Sportstech, Fintech, AI"
            value={formData.domain}
            onChange={handleChange}
            required
            className="h-12 text-lg px-4"
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="location">Location</Label>
          <Input
            id="location"
            name="location"
            placeholder="e.g., Bangalore, New York, London"
            value={formData.location}
            onChange={handleChange}
            required
            className="h-12 text-lg px-4"
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="role">Role</Label>
          <Input
            id="role"
            name="role"
            placeholder="e.g., Founder, CEO, CTO"
            value={formData.role}
            onChange={handleChange}
            required
            className="h-12 text-lg px-4"
          />
        </div>
      </div>

      <Button type="submit" className="w-full h-12 text-lg font-medium" disabled={isLoading}>
        {isLoading ? 'Searching...' : 'Find Founders'}
      </Button>
    </form>
  );
};

export default SearchForm;
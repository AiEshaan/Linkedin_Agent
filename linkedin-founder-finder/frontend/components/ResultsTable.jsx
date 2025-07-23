import React from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';

const ResultsTable = ({ results, query }) => {
  if (!results || results.length === 0) {
    return null;
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableCaption>Search query: {query}</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>LinkedIn URL</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {results.map((founder, index) => (
            <TableRow key={index}>
              <TableCell className="font-medium">{founder.name}</TableCell>
              <TableCell>
                <a
                  href={founder.linkedin_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {founder.linkedin_url}
                </a>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ResultsTable;
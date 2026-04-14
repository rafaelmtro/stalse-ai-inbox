This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Frontend Stack

- **Next.js (App Router)**: React framework for server-side rendering and static site generation.
- **TypeScript**: Ensuring type safety across the application.
- **TailwindCSS**: Utility-first CSS framework for rapid UI development.
- **Recharts**: For data visualization on the dashboard.
- **Jest & React Testing Library**: For comprehensive unit and integration testing.

## Project Structure

```text
frontend/
├── __tests__/           # Unit and integration tests (Jest)
├── public/              # Static assets (images, icons, etc.)
└── src/
    ├── app/             # Next.js App Router (pages and layouts)
    ├── components/      # Reusable UI components
    ├── lib/             # API client and utility functions
    ├── types/           # TypeScript type definitions
    └── globals.css      # Global styles and Tailwind imports
```

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!


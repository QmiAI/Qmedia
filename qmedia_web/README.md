## Qmedia web

**English** | [简体中文](./README.zh-CN.md)

### Tech Stack

- Language: [Typescript](https://www.typescriptlang.org/)
- Framework: [Next.js](https://nextjs.org/)
- Styling: [tailwindcss](https://tailwindcss.com/)
- Components: [shadcn/ui](https://ui.shadcn.com/)

### Installation Instructions

#### Setup Environment

**nvm**

Refer to https://github.com/nvm-sh/nvm#install--update-script

**nodejs**

```bash
nvm install node
```

**pnpm**

Refer to https://pnpm.io/installation

#### Install Dependencies

```bash
pnpm install
```

#### Modify Configuration File

```bash
cp .env.example .env
```

Set the port number of `SERVICE_ENDPOINT` in the `.env` file to the port number of qmedia_web.

#### Run the Service

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

<div align="right">

[![][back-to-top]](../README.md)

</div>

[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square

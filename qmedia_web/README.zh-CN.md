## Qmedia web

**简体中文** | [English](./README.md)

### 技术栈

- 语言: [Typescript](https://www.typescriptlang.org/)
- 框架: [Next.js](https://nextjs.org/)
- 样式: [tailwindcss](https://tailwindcss.com/)
- 组件: [shadcn/ui](https://ui.shadcn.com/)

### 安装说明

#### 安装环境

**nvm**

参考 https://github.com/nvm-sh/nvm#install--update-script

**nodejs**

```bash
nvm install node
```

**pnpm**

参考 https://pnpm.io/installation

#### 依赖安装

```bash
pnpm install
```

#### 修改 配置文件

```bash
cp .env.example .env
```

将 .env 中 SERVICE_ENDPOINT 的端口号设置为 qmedia_web 的端口号

#### 运行服务

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

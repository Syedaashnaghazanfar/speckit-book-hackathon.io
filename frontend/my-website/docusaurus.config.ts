import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: "Physical AI & Humanoid Robotics",
  tagline: "Master the future of AI-powered robotics with hands-on learning",
  favicon: "img/ai.png",

  // ✅ ✅ ✅ MERMAID ENABLED HERE
  markdown: {
    mermaid: true,
  },

  // ✅ ✅ ✅ MERMAID THEME ADDED HERE
  themes: ["@docusaurus/theme-mermaid"],

  future: {
    v4: true,
  },

  url: "https://your-docusaurus-site.example.com",
  baseUrl: "/",

  organizationName: "your-org",
  projectName: "physical-ai-textbook",

  onBrokenLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl:
            "https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/",
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ["rss", "atom"],
            xslt: true,
          },
          editUrl:
            "https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/",
          onInlineTags: "warn",
          onInlineAuthors: "warn",
          onUntruncatedBlogPosts: "warn",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: "img/physical-ai-comparation.png",
    colorMode: {
      defaultMode: "dark",
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: "Physical AI Textbook",
      logo: {
        alt: "Physical AI Robot Logo",
        src: "img/ai.png",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Course Modules",
        },
        {
          href: "https://github.com/Syedaashnaghazanfar/speckit-book-hackathon.io",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Course Content",
          items: [
            { label: "Get Started", to: "/docs/intro" },
            {
              label: "Module 1: ROS 2",
              to: "/docs/module-1-ros2/week-01-intro-physical-ai",
            },
            {
              label: "Module 2: Gazebo",
              to: "/docs/module-2-gazebo/week-06-gazebo-fundamentals",
            },
            {
              label: "Module 3: Isaac",
              to: "/docs/module-3-isaac/week-08-isaac-intro",
            },
          ],
        },
        {
          title: "Advanced Topics",
          items: [
            {
              label: "Module 4: VLA",
              to: "/docs/module-4-vla/week-11-humanoid-development",
            },
            {
              label: "Humanoid Development",
              to: "/docs/module-4-vla/week-11-humanoid-development",
            },
            {
              label: "Capstone Project",
              to: "/docs/module-4-vla/week-13-conversational-robotics-capstone",
            },
          ],
        },
        {
          title: "Resources",
          items: [
            {
              label: "GitHub Repository",
              href: "https://github.com/Syedaashnaghazanfar/speckit-book-hackathon.io",
            },
            {
              label: "NVIDIA Isaac",
              href: "https://developer.nvidia.com/isaac",
            },
            { label: "ROS 2 Documentation", href: "https://docs.ros.org/" },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Made by Ashna Ghazanfar.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

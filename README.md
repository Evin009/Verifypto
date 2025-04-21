# Crypto

# Inspiration sample
With the rise of cryptocurrency adoption, scams and shady crypto projects have become a growing concern, especially for beginners. We wanted to build something that could act as a trustworthy watchdog for the blockchain, helping users detect potentially risky or fraudulent crypto wallets and contracts in real time. Our goal was to create a tool that promotes transparency, awareness, and safety in the crypto world.

# What it does
Verifypto is an AI-powered crypto verification tool that lets users check the credibility of Ethereum wallets and smart contracts.

it: Detects whether a wallet is an individual or a contract Analyzes transaction activity, token transfers, and contract source code Flags red flags like blacklist functions, onlyOwner privileges, and unverified contracts Rates the risk level (Safe, Medium Risk, or Likely Scam) using Google Gemini AI Stores verification history and lets users view their past lookups

In short, Verifypto helps users avoid scams and make informed decisions in Web3.

# How we built it
Backend: Python + Flask Smart Contract Analysis: Etherscan APIs (for transactions, contract source, token supply) AI Analysis: Google Gemini API to summarize risks and generate verdicts Database: MongoDB Atlas to store verification history Deployment: Ngrok for quick public API tunneling We wrote custom logic to calculate on-chain risk scores, and Gemini helped us translate raw data into human-friendly insights.

#Challenges we ran into
- Making sure the app could reliably distinguish wallets from contracts.
- Interpreting raw blockchain data into meaningful risk indicators.
- Crafting prompts that Gemini could understand consistently.
- Handling edge cases like trusted tokens (e.g., USDT, USDC) being flagged unfairly.
- Learning how to use multiple APIs and services together smoothly.

# Accomplishments that we're proud of
Our app successfully catches red flags in known scam contracts! It gives easy-to-understand summaries of technical blockchain data. Built a working product from scratch with a team of beginner developers in < 24 hours! Learned a lot about smart contract analysis, AI prompt engineering, and real-world security concerns in Web3.


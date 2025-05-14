# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a hotel booking and invoice management system using LlamaIndex with a PostgreSQL database. It creates AI agents that help users search for hotels, make bookings, update check-in/checkout dates, cancel reservations, and manage invoices.

## Architecture

The system consists of:

1. LlamaIndex agent workflows powered by Google's Gemini LLM (with option for Anthropic's Claude)
2. A PostgreSQL database for storing hotel and invoice information
3. Database tools defined in YAML for hotel and invoice operations
4. A Toolbox client to load and use these tools

## Components

- `hotel_agent.py`: Application script that sets up an agent workflow for hotel operations
- `invoices.py`: Application script that sets up an agent workflow for invoice management
- `tools.yaml`: Defines database operations as tools that can be used by the agents:
  - Hotel tools:
    - `search-hotels-by-name`
    - `search-hotels-by-location`
    - `book-hotel`
    - `update-hotel`
    - `cancel-hotel`
  - Invoice tools:
    - `list-invoices`
    - `create-invoice`
    - `update-invoice-status`

## Dependencies

- LlamaIndex for the agent framework
- PostgreSQL for database storage
- Google Gemini API (or optionally Anthropic API) for the LLM

## Environment Setup

Requires:
- PostgreSQL database running with appropriate schema
- Environment variables:
  - `GOOGLE_API_KEY` (if using Gemini)
  - `ANTHROPIC_API_KEY` (if using Claude)

## Running the Applications

First, start the toolbox server:
```
~/bin/toolbox --tools-file "tools.yaml"
```

To run the hotel agent demo:
```
python hotel_agent.py
```

To run the invoice management demo:
```
python invoices.py
```

Both applications connect to a PostgreSQL database at `127.0.0.1:5432` and a Toolbox server at `http://127.0.0.1:5000`.

## Database Schema

The system uses two main tables:

1. `hotels` table with columns:
   - id
   - name
   - location
   - booked (boolean)
   - checkin_date
   - checkout_date

2. `invoices` table with columns:
   - id
   - hotel_id
   - guest_name
   - amount
   - invoice_date
   - paid (boolean)
   - created_at
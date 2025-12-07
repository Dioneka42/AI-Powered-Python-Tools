#!/usr/bin/env python3
"""
Financial Historical Novel Research Assistant
Deep dive research tool for historical financial fiction writing
"""

import json
import os
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic library not installed.")
    print("Please run: pip install anthropic")
    exit(1)

API_KEY_FILE = '.novel_research_api_key.json'
RESEARCH_LOG_FILE = 'novel_research_log.json'


def save_api_key(api_key):
    """Save API key to file"""
    with open(API_KEY_FILE, 'w') as f:
        json.dump({'api_key': api_key}, f)


def load_api_key():
    """Load API key from file"""
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            data = json.load(f)
            return data.get('api_key')
    return None


def get_api_key():
    """Get API key from file, environment variable, or user input"""
    api_key = load_api_key()
    
    if api_key:
        return api_key
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("\n" + "="*70)
        print("ANTHROPIC API KEY REQUIRED")
        print("="*70)
        print("You need an API key from: https://console.anthropic.com")
        print("Your API key will be saved securely for future use.")
        print("="*70)
        api_key = input("\nEnter your Anthropic API key: ").strip()
        
        if api_key:
            save_api_key(api_key)
            print("✓ API key saved successfully!")
    
    return api_key


def deep_research(topic, time_period, api_key):
    """Conduct deep research on a topic"""
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*70}")
    print(f"RESEARCHING: {topic.upper()}")
    print(f"Period: {time_period}")
    print(f"{'='*70}")
    print("Analyzing topic and conducting deep dive research...")
    print("This may take 3-5 minutes.\n")
    
    # Universal prompt that auto-detects category
    prompt = f"""You are a research assistant for a novelist writing financial historical fiction. Analyze this research request and provide comprehensive research tailored to fiction writing.

RESEARCH TOPIC: {topic}
TIME PERIOD: {time_period}

First, intelligently determine what TYPE of research this is:
- Is it a historical event (crash, scandal, deal, crisis)?
- Is it a financial system/instrument (how something worked)?
- Is it character development (person, role, profession)?
- Is it a setting/location (place, building, district)?
- Is it something else entirely?

Then provide EXCEPTIONALLY DETAILED research covering ALL aspects relevant for writing historical fiction:

**Core Information:**
- Historical facts and timeline with specific dates
- Key figures involved with detailed profiles (personalities, backgrounds, quirks, speech patterns)
- How things actually worked (mechanisms, processes, step-by-step)
- Cultural and social context of the period

**For Fiction Writing:**
- Sensory details (sights, sounds, smells, textures, atmosphere)
- Period-appropriate dialogue examples and jargon
- Dramatic moments and turning points that would make great scenes
- Human conflicts, tensions, rivalries, and relationships
- Lesser-known fascinating details that add authenticity
- Character motivations and emotional stakes
- Physical descriptions of places, people, and objects

**Authenticity:**
- What regular people experienced and thought
- Social hierarchies and class dynamics
- Daily life details and routines
- Technology and infrastructure of the time
- What existed vs. what would be anachronistic
- Primary sources (letters, diaries, newspapers, testimonies)
- Contemporary language and how people spoke

**Dramatic Potential:**
- Most dramatic/tension-filled moments
- Personal tragedies and triumphs
- Shocking revelations or turning points
- Conflicts between characters/groups
- Stakes and consequences

Provide the level of detail a novelist needs to write vivid, authentic, engaging scenes. Focus on bringing history to life through human drama, sensory experience, and authentic period flavor. Be extremely specific and comprehensive."""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        research = message.content[0].text
        return research
    
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def old_deep_research_prompts_backup():
    """Backup of old categorical prompts - kept for reference"""
    prompts = {
        'historical_event': f"""Provide an exceptionally detailed research report on this historical financial event for use in writing historical fiction:

TOPIC: {topic}
TIME PERIOD: {time_period}

Please provide comprehensive information covering:

1. **Timeline & Key Dates**: Detailed chronology of events leading up to, during, and after the event. Include specific dates, times when relevant, and the sequence of critical moments.

2. **Key Figures & Characters**: Detailed profiles of the main people involved - their backgrounds, personalities, motivations, relationships, what they wore, how they spoke, their habits and quirks. Include both famous figures and lesser-known players who would make interesting characters.

3. **The Financial Mechanics**: Explain in detail HOW the financial aspects worked. What were the specific transactions, instruments, strategies, loopholes, or innovations? Break down complex financial concepts into understandable terms while maintaining accuracy.

4. **Cultural & Social Context**: What was daily life like during this period? Fashion, technology, social norms, popular culture, political climate, economic conditions for regular people. Paint a vivid picture of the era.

5. **Locations & Settings**: Describe the specific places where events unfolded - trading floors, offices, mansions, streets, cities. Include architectural details, atmosphere, sounds, smells. What did these places look and feel like?

6. **Dialogue & Language**: How did people speak in this era? Include period-appropriate phrases, financial jargon of the time, slang, and speech patterns. Provide examples of authentic dialogue.

7. **Dramatic Moments**: Identify the most dramatic, tension-filled moments that would make great scenes. What were the turning points? The moments of crisis? The shocking revelations?

8. **Lesser-Known Details**: Share fascinating historical details, anecdotes, and facts that aren't widely known but would add authenticity and richness to a novel.

9. **Primary Sources**: Mention letters, diaries, newspaper articles, testimonies, or other primary sources from the time that could inspire authentic dialogue and scenes.

10. **Conflicts & Tensions**: What were the human conflicts, rivalries, alliances, and betrayals? Who opposed whom and why? What were the personal stakes?

Be extremely detailed and specific. This is for fiction writing, so focus on elements that bring the history to life - sensory details, human drama, authentic period flavor.""",

        'financial_system': f"""Provide an in-depth explanation of this financial system, instrument, or practice for use in historical fiction:

TOPIC: {topic}
TIME PERIOD: {time_period}

Please provide comprehensive information covering:

1. **How It Actually Worked**: Explain the mechanics in detail - step by step, who did what, where money/assets moved, what documents were involved, what the process looked like in practice.

2. **Who Used It & Why**: Which types of people or institutions used this system? What were their motivations? What advantages did it provide? What risks did it carry?

3. **Physical Details**: What did it look like in practice? What papers were signed? Where did transactions occur? What tools or technology were used? Describe the physical process.

4. **The Players Involved**: Who were the key roles - traders, brokers, bankers, clerks, regulators? What did each person do? What was their typical background and personality?

5. **Historical Evolution**: How did this system develop? What came before it? How did it change over time? What events shaped its evolution?

6. **Jargon & Terminology**: What were the specific terms, slang, and phrases used? Provide a glossary of period-appropriate language that would help authentic dialogue.

7. **Rules & Regulations**: What were the formal and informal rules? How were things "supposed" to work versus how they actually worked? Where were the loopholes?

8. **Risks & Scandals**: What could go wrong? What were common abuses or frauds? Include specific historical examples of things going sideways.

9. **Daily Operations**: What did a typical day look like for someone working in this system? Walk through a normal transaction or workday.

10. **Cultural Significance**: What did this financial practice mean to society at the time? How did regular people view it? What controversies surrounded it?

Provide extremely specific, practical details that would help a novelist write realistic scenes involving this financial system.""",

        'character_research': f"""Provide detailed research for developing an authentic historical character:

CHARACTER TYPE: {topic}
TIME PERIOD: {time_period}

Please provide comprehensive information covering:

1. **Daily Life & Routine**: What would a typical day look like? When did they wake up? What did they eat? How did they get around? What was their work schedule?

2. **Education & Background**: What education would they have had? What books would they have read? What skills and knowledge were expected? How did they enter their profession?

3. **Social Status & Class**: Where did they fit in the social hierarchy? Who could they associate with? What were the class boundaries and social expectations?

4. **Wealth & Possessions**: What could they afford? What would their home look like? What would they own? How did they display (or hide) their wealth?

5. **Fashion & Appearance**: What would they wear in different situations? How did men/women of this type dress? What accessories, grooming, and style were typical?

6. **Speech & Mannerisms**: How would they speak? What accent or dialect? What phrases would they use? What were their typical mannerisms and behaviors?

7. **Values & Beliefs**: What did they believe in? What were their values, prejudices, and blind spots typical of their time and position?

8. **Professional Life**: What did their work actually entail? What tools did they use? Who did they interact with? What were their professional challenges?

9. **Relationships & Social Life**: Who would they know? How did they socialize? What clubs, venues, or gatherings would they attend? How did they network?

10. **Personal Struggles**: What pressures and conflicts would someone in this position face? What kept them up at night? What were their ambitions and fears?

11. **Historical Examples**: Provide specific examples of real people who fit this profile, including details about their lives that could inspire fictional characters.

Be extremely detailed and specific to help create an authentic, three-dimensional character.""",

        'setting_research': f"""Provide immersive research on this historical setting for fiction writing:

LOCATION/SETTING: {topic}
TIME PERIOD: {time_period}

Please provide comprehensive information covering:

1. **Physical Description**: Detailed description of the location - architecture, layout, landmarks, streets, buildings. What did it look, smell, sound, and feel like?

2. **Atmosphere & Mood**: What was the general atmosphere? Was it bustling or quiet? Dangerous or safe? Formal or casual? Describe the energy and feeling of the place.

3. **Who Was There**: What types of people frequented this location? What were they doing? How did they interact? What was the social dynamic?

4. **Daily Rhythms**: How did the setting change throughout the day? Morning to night? Weekday versus weekend? Different seasons?

5. **Technology & Infrastructure**: What technology existed? How did things work (lighting, heating, communication, transportation)? What modern conveniences did NOT exist?

6. **Sensory Details**: Specific sounds (what could you hear?), smells (what did the air smell like?), textures, temperatures, lighting conditions throughout different times.

7. **Social Geography**: Where did different classes of people go? Which areas were respectable or disreputable? What were the invisible social boundaries?

8. **Notable Events**: What typically happened here? Were there regular events, rituals, or occurrences? Any famous historical events at this location?

9. **Insider Knowledge**: What would only locals know? Secret shortcuts? Unwritten rules? Ways to spot an outsider? Local customs and quirks?

10. **Period Details**: What specific details would mark this as being from this exact time period? What would be anachronistic? What was brand new versus old-fashioned?

11. **Dramatic Potential**: What conflicts, tensions, or dramas naturally arose in this setting? What made it an interesting or dangerous place to be?

Provide vivid, immersive details that would help a novelist place readers directly in this setting.""",

        'financial_crisis': f"""Provide comprehensive research on this financial crisis or panic for historical fiction:

CRISIS: {topic}
TIME PERIOD: {time_period}

Please provide detailed information covering:

1. **The Build-Up**: What conditions led to the crisis? What warning signs were ignored? Who saw it coming and who didn't? Detail the mounting pressure.

2. **The Breaking Point**: What specifically triggered the crisis? What was the "oh shit" moment? Describe the exact sequence of events when everything fell apart.

3. **The Panic Spreads**: How did panic spread? Who panicked first? How did information (and misinformation) travel? What did panic look and feel like?

4. **Key Moments**: Identify the most dramatic moments - bank runs, emergency meetings, desperate decisions, suicide, fortunes lost overnight, stunning revelations.

5. **Heroes & Villains**: Who were the heroes who tried to solve it? Who were the villains who caused or profited from it? Who were the victims? Provide detailed profiles.

6. **The Human Cost**: What happened to regular people? Who lost everything? What were the stories of personal tragedy? How did it affect daily life?

7. **The Response**: How did authorities respond? What emergency measures were taken? What worked and what failed? Who resisted and why?

8. **Market Mechanics**: Explain the specific financial mechanics of what went wrong. How did the dominoes fall? What interconnections caused contagion?

9. **Contemporary Accounts**: What did newspapers report? What did people write in letters and diaries? How did people understand (or misunderstand) what was happening?

10. **Long-Term Impact**: What changed afterward? What lessons were learned (or not learned)? How did it reshape the financial system?

11. **Dramatic Scenes**: Identify specific moments, conversations, or confrontations that would make powerful scenes in a novel.

Provide the level of detail needed to write gripping, authentic scenes about this crisis.""",

        'custom': f"""Conduct deep research on this topic for a financial historical novel:

RESEARCH TOPIC: {topic}
TIME PERIOD: {time_period}

Please provide exceptionally detailed research covering all aspects relevant to writing historical fiction:

- Historical accuracy and factual details
- Cultural and social context of the period
- Key figures, personalities, and character types
- Physical settings and sensory descriptions
- Period-appropriate language and dialogue
- Financial mechanisms and systems in detail
- Dramatic moments and human conflicts
- Lesser-known fascinating details
- Primary sources and historical accounts
- Authentic period flavor and atmosphere

Provide comprehensive, specific, practical information that would help a novelist write vivid, accurate, engaging historical fiction about this topic. Focus on details that bring the history to life - the human drama, the sensory experience, the authentic period details."""
    }
    
    prompt = prompts.get(research_type, prompts['custom'])
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        research = message.content[0].text
        return research
    
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def display_research(topic, research):
    """Display research results"""
    print(f"\n{'='*70}")
    print(f"RESEARCH REPORT: {topic.upper()}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print(f"{'='*70}\n")
    print(research)
    print(f"\n{'='*70}")


def save_research(topic, research, time_period):
    """Save research to log file"""
    log_data = []
    
    if os.path.exists(RESEARCH_LOG_FILE):
        with open(RESEARCH_LOG_FILE, 'r') as f:
            log_data = json.load(f)
    
    entry = {
        'topic': topic,
        'time_period': time_period,
        'timestamp': datetime.now().isoformat(),
        'research': research
    }
    
    log_data.append(entry)
    
    with open(RESEARCH_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def export_research(topic, research, time_period):
    """Export research to text file"""
    filename = f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"RESEARCH REPORT: {topic.upper()}\n")
        f.write(f"Time Period: {time_period}\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("="*70 + "\n\n")
        f.write(research)
        f.write("\n\n" + "="*70 + "\n")
        f.write("Generated by Financial Historical Novel Research Assistant\n")
    
    print(f"\n✓ Research exported to: {filename}")


def view_past_research():
    """View past research"""
    if not os.path.exists(RESEARCH_LOG_FILE):
        print("\nNo past research found.")
        return
    
    with open(RESEARCH_LOG_FILE, 'r') as f:
        log_data = json.load(f)
    
    if not log_data:
        print("\nNo past research found.")
        return
    
    print(f"\n{'='*70}")
    print("RESEARCH HISTORY")
    print(f"{'='*70}")
    print(f"{'#':<5} {'Topic':<35} {'Period':<20} {'Date':<20}")
    print('-'*70)
    
    for i, entry in enumerate(reversed(log_data), 1):
        dt = datetime.fromisoformat(entry['timestamp'])
        topic = entry['topic'][:33] + '..' if len(entry['topic']) > 35 else entry['topic']
        period = entry['time_period'][:18] + '..' if len(entry['time_period']) > 20 else entry['time_period']
        print(f"{i:<5} {topic:<35} {period:<20} {dt.strftime('%b %d, %Y'):<20}")
    
    print('='*70)
    
    choice = input("\nEnter research number to view (or press Enter to go back): ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(log_data):
            entry = list(reversed(log_data))[idx]
            display_research(entry['topic'], entry['research'])
            
            export = input("\nExport this research? (y/n): ").strip().lower()
            if export == 'y':
                export_research(entry['topic'], entry['research'], entry['time_period'])
        else:
            print("Invalid selection.")


def main():
    """Main function"""
    print("="*70)
    print("FINANCIAL HISTORICAL NOVEL RESEARCH ASSISTANT")
    print("Deep Dive Research Tool for Fiction Writers")
    print("="*70)
    
    api_key = get_api_key()
    
    if not api_key:
        print("\nNo API key provided. Exiting.")
        return
    
    print("\n✓ API key loaded successfully!")
    
    while True:
        print("\n" + "="*70)
        print("OPTIONS")
        print("="*70)
        print("1. Research a topic")
        print("2. View past research")
        print("3. Delete saved API key")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            print("\n" + "="*70)
            print("WHAT TO RESEARCH")
            print("="*70)
            print("Examples:")
            print("- '1929 Stock Market Crash'")
            print("- 'Wall Street trader in the 1920s'")
            print("- 'NYSE trading floor atmosphere'")
            print("- 'How stock certificates worked in 1890'")
            print("- 'Panic of 1907'")
            print("- 'JP Morgan's personality and leadership style'")
            print("- 'Life of a bank clerk in Victorian London'")
            print("="*70)
            
            topic = input("\nWhat do you want to research?\n> ").strip()
            
            if not topic:
                print("No topic provided.")
                continue
            
            time_period = input("\nTime period (e.g., '1920s', '1907', 'Gilded Age'):\n> ").strip()
            
            if not time_period:
                time_period = "Historical period not specified - please use context from topic"
            
            # Conduct research
            research = deep_research(topic, time_period, api_key)
            display_research(topic, research)
            
            # Save research
            save_research(topic, research, time_period)
            print("\n✓ Research saved to log!")
            
            # Export option
            export = input("\nExport to text file? (y/n): ").strip().lower()
            if export == 'y':
                export_research(topic, research, time_period)
        
        elif choice == '2':
            view_past_research()
        
        elif choice == '3':
            if os.path.exists(API_KEY_FILE):
                confirm = input("\nDelete saved API key? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    os.remove(API_KEY_FILE)
                    print("\n✓ API key deleted!")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("\nNo saved API key found.")
        
        elif choice == '4':
            print("\nHappy writing! 📚✍️")
            break
        
        else:
            print("Invalid option. Please select 1-4.")


if __name__ == "__main__":
    main()

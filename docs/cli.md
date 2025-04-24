# DMForge CLI Reference

## `dmforge`
**Help:** DMForge CLI – Generate spell decks, scenes, and more.

```shell
Usage: dmforge [OPTIONS] COMMAND [ARGS]...                                                                                                                                                      
                                                                                                                                                                                                 
 DMForge CLI – Generate spell decks, scenes, and more.                                                                                                                                           
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --env                       TEXT  Override environment [default: None]                                                                                                                        │
│ --install-completion              Install completion for the current shell.                                                                                                                   │
│ --show-completion                 Show completion for the current shell, to copy it or customize the installation.                                                                            │
│ --help                            Show this message and exit.                                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ docs-cli   Generate CLI reference documentation.                                                                                                                                              │
│ version    Show DMForge version and active environment.                                                                                                                                       │
│ help       Show system overview, CLI usage, and dev docs.                                                                                                                                     │
│ fetch      Data fetching commands                                                                                                                                                             │
│ deck       Generate and render spell card decks                                                                                                                                               │
│ prompt     Generate individual prompts                                                                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge version`
```shell
Usage: dmforge version [OPTIONS]                                                                                                                                                                
                                                                                                                                                                                                 
 Show DMForge version and active environment.                                                                                                                                                    
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge help`
```shell
Usage: dmforge help [OPTIONS]                                                                                                                                                                   
                                                                                                                                                                                                 
 Show system overview, CLI usage, and dev docs.                                                                                                                                                  
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge docs-cli`
```shell
Usage: dmforge docs-cli [OPTIONS]                                                                                                                                                               
                                                                                                                                                                                                 
 Generate CLI reference documentation.                                                                                                                                                           
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge fetch`
```shell
Usage: dmforge fetch [OPTIONS] COMMAND [ARGS]...                                                                                                                                                
                                                                                                                                                                                                 
 Data fetching commands                                                                                                                                                                          
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ srd   Download and cache SRD data from dnd5eapi.co.                                                                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge fetch srd`
```shell
Usage: dmforge fetch srd [OPTIONS]                                                                                                                                                              
                                                                                                                                                                                                 
 Download and cache SRD data from dnd5eapi.co.                                                                                                                                                   
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --spells            Fetch SRD spells                                                                                                                                                          │
│ --traits            Fetch racial traits                                                                                                                                                       │
│ --features          Fetch class features                                                                                                                                                      │
│ --all               Fetch all available SRD content                                                                                                                                           │
│ --force             Force re-download and overwrite                                                                                                                                           │
│ --help              Show this message and exit.                                                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge deck`
```shell
Usage: dmforge deck [OPTIONS] COMMAND [ARGS]...                                                                                                                                                 
                                                                                                                                                                                                 
 Generate and render spell card decks                                                                                                                                                            
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ build    Build a full or filtered SRD spell deck, optionally with interactive selection.                                                                                                      │
│ render   Render a deck to PDF or HTML, optionally summarizing descriptions first.                                                                                                             │
│ art      Generate DALL·E art for each card in a deck JSON and update its art_url.                                                                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge deck build`
```shell
Usage: dmforge deck build [OPTIONS]                                                                                                                                                             
                                                                                                                                                                                                 
 Build a full or filtered SRD spell deck, optionally with interactive selection.                                                                                                                 
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                TEXT     Output file name [default: deck.json]                                                                                                        │
│ --limit           -n                    INTEGER  Limit N spells [default: None]                                                                                                               │
│ --summarize           --no-summarize             Summarize descriptions [default: no-summarize]                                                                                               │
│ --summary-length                        INTEGER  Max chars for summary [default: 250]                                                                                                         │
│ --class                                 TEXT     Filter by class (comma-separated) [default: None]                                                                                            │
│ --level                                 TEXT     Filter by spell level(s) [default: None]                                                                                                     │
│ --school                                TEXT     Filter by school(s) [default: None]                                                                                                          │
│ --interactive                                    Select spells interactively                                                                                                                  │
│ --help                                           Show this message and exit.                                                                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge deck art`
```shell
Usage: dmforge deck art [OPTIONS] DECK_FILE                                                                                                                                                     
                                                                                                                                                                                                 
 Generate DALL·E art for each card in a deck JSON and update its art_url.                                                                                                                        
                                                                                                                                                                                                 
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    deck_file      PATH  Deck JSON file to enrich with art [default: None] [required]                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --art-dir        PATH     Where to save generated images [default: assets\art]                                                                                                                │
│ --size           TEXT     Image size for DALL·E [default: 512x512]                                                                                                                            │
│ --n              INTEGER  Number of images per card (always uses first) [default: 1]                                                                                                          │
│ --help                    Show this message and exit.                                                                                                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge deck render`
```shell
Usage: dmforge deck render [OPTIONS] DECK_FILE                                                                                                                                                  
                                                                                                                                                                                                 
 Render a deck to PDF or HTML, optionally summarizing descriptions first.                                                                                                                        
                                                                                                                                                                                                 
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    deck_file      PATH  Deck JSON file to render [default: None] [required]                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --format                              TEXT     Output format (pdf or html) [default: pdf]                                                                                                     │
│ --layout                              TEXT     Layout: sheet or cards [default: sheet]                                                                                                        │
│ --output                              TEXT     Output file path [default: None]                                                                                                               │
│ --theme                               TEXT     Theme to use [default: default]                                                                                                                │
│ --debug                                        Also write raw HTML for inspection                                                                                                             │
│ --summarize         --no-summarize             Summarize descriptions before rendering [default: no-summarize]                                                                                │
│ --summary-length                      INTEGER  Max chars for summary (default 250) [default: 250]                                                                                             │
│ --help                                         Show this message and exit.                                                                                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge prompt`
```shell
Usage: dmforge prompt [OPTIONS] COMMAND [ARGS]...                                                                                                                                               
                                                                                                                                                                                                 
 Generate individual prompts                                                                                                                                                                     
                                                                                                                                                                                                 
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ show   Show AI art prompt for a single spell by index or name.                                                                                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## `dmforge prompt show`
```shell
Usage: dmforge prompt show [OPTIONS] IDENTIFIER                                                                                                                                                 
                                                                                                                                                                                                 
 Show AI art prompt for a single spell by index or name.                                                                                                                                         
                                                                                                                                                                                                 
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    identifier      TEXT  Spell index or name [default: None] [required]                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --suffix  -s      TEXT  Suffix for prompt                                                                                                                                                     │
│ --help                  Show this message and exit.                                                                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

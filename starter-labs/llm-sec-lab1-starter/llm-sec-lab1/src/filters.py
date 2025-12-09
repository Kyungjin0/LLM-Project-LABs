import re

def basic_input_filter(s: str) -> str:
    """
    Filter out common prompt injection patterns and role-playing attempts.
    This is a basic filter - the LLM should also have strong refusal policies.
    """
    s = s.strip()
    
    # Common prompt injection patterns
    s = re.sub(r'(?i)ignore (all|previous|any|the) (instructions?|prompts?|directives?)', '[redacted-injection]', s)
    s = re.sub(r'(?i)forget (all|previous|everything)', '[redacted-injection]', s)
    s = re.sub(r'(?i)disregard (all|previous)', '[redacted-injection]', s)
    
    # Role-playing attempts
    s = re.sub(r'(?i)(you are|you\'re) (now|the|a) (system|developer|admin|assistant|AI)', '[role-play-blocked]', s)
    s = re.sub(r'(?i)as (system|developer|admin):', '[role-play-blocked]', s)
    s = re.sub(r'(?i)act (as|like) (a|an|the)', '[role-play-blocked]', s)
    s = re.sub(r'(?i)pretend (you are|to be)', '[role-play-blocked]', s)
    
    # Behavior change attempts
    s = re.sub(r'(?i)(change|modify|alter|disable) (your|the) (behavior|safeguards?|rules?|policies?)', '[behavior-change-blocked]', s)
    s = re.sub(r'(?i)(disable|remove|turn off) (safeguards?|safety|security)', '[safety-disable-blocked]', s)
    
    # System prompt manipulation
    s = re.sub(r'(?i)system\s*:', '[system-prefix-blocked]', s)
    s = re.sub(r'(?i)developer\s*:', '[developer-prefix-blocked]', s)
    
    # Instruction embedding attempts
    s = re.sub(r'(?i)(new|override|replace) (instructions?|prompts?|directives?)', '[instruction-override-blocked]', s)

    # Leading verbs that try to steer behavior (so downstream sees it as potential injection)
    s = re.sub(r'(?i)^(summarize|classify|execute|run|perform)\s*:', '[embedded-instruction]:', s)
    s = re.sub(r'(?i)\b(as system|as developer)\b', '[role-play-blocked]', s)

    # External fetch / follow instructions attempts
    s = re.sub(r'(?i)(browse|fetch|visit|open)\s+https?://', '[external-fetch-blocked] ', s)
    s = re.sub(r'(?i)follow its instructions', '[external-instructions-blocked]', s)

    # Exfiltration / sensitive data asks
    s = re.sub(r'(?i)(secret|password|api key|token)', '[sensitive-request]', s)
    s = re.sub(r'(?i)(email|send|exfiltrate)', '[exfiltration-attempt]', s)
    
    return s

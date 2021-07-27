from helpers.namespaces import CURIES

def _make_fragment_uri(g, owl_class):
    parsed_uri={}
    parsed_uri['name'] = get_last_segment_of_uri(owl_class)
    parsed_uri['namespace'] = get_uri_namespace(str(owl_class))
    parsed_uri['prefix'] = get_uri_prefix(parsed_uri['namespace'], g)
    return parsed_uri

def get_uri_namespace(uri : str):
    # Get the URI namespace by dropping the '#'.
    URI = str(uri).split('#')[0]

    if URI == str(uri):
        # If URI unchanged, it means the separator is a '/'. Go ahead and drop the word after the slash.
        suffix = URI.split('/')[-1]
        URI = URI.replace(suffix, '')
    else:
        # Append the '#' back on so it ends in a hash or slash.
        URI += '#'
    #print(URI)
    return URI

def get_last_segment_of_uri(uri : str):
    return str(uri).split('#')[-1].split('/')[-1]

def get_uri_prefix(uri : str, g):
    # Get the prefix of the URI.
    prefix = ''
    for k, v in CURIES.items():
        if v == uri:
            prefix = k
            #print(prefix)
            return prefix

    # Nothing was found, just return an empty string.
    return prefix
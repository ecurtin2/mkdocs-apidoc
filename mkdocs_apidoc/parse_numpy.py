from inspect import isfunction

from numpydoc.docscrape import ClassDoc, FunctionDoc


def from_numpy(obj: object) -> str:

    if isfunction(obj):
        doc = FunctionDoc(obj)

        params = doc["Parameters"]
        ps = [f"### {p.name}\n\n{' '.join(p.desc)}" for p in params]
        params_section = "\n\n" + "\n\n".join(ps) + "\n\n"
        return (
            " ".join(doc["Summary"])
            + "\n\n"
            + " ".join(doc["Extended Summary"])
            + params_section
        )

    else:
        doc = ClassDoc(obj)
        return str([p.name for p in doc["Parameters"]])

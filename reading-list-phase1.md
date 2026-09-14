# Structured Meeting Intelligence : Core Reading List, Phase 1

## For all to read

## 1. Shriberg, Dhillon, Bhagat, Ang & Carvey (2004)
### *The ICSI Meeting Recorder Dialog Act (MRDA) Corpus*

**SIGDIAL 2004**  
https://aclanthology.org/W04-2319/

### Why I think we need this

This is the primary paper for the dataset we are actually developing on. Before we design the classifier, we need to be completely clear about what the ICSI annotations mean and how they are represented in the raw data.

The annotation scheme includes the dialogue-act labels, continuation markers, and adjacency-pair information that our preprocessing and later chain-linking stage will depend on.

I do not want us to build a clean-looking parser while misunderstanding the original annotation format. This paper should therefore be treated as a **data-format and annotation reference**, not just another related-work paper.


### Required companion

The paper should be read together with:

**Dhillon, Bhagat, Carvey & Shriberg (2004), *Meeting Recorder Project: Dialog Act Labeling Guide*, ICSI TR-04-002.**

The guide is important because it gives the detailed annotation definitions we need when mapping the original ICSI labels into our own three event types.

---

## 2. Żelasko, Pappagari & Dehak (2021)
### *What Helps Transformers Recognize Conversational Structure? Importance of Context, Punctuation, and Labels in Dialog Act Recognition*

**Transactions of the ACL, Vol. 9, pp. 1163–1179**  
https://doi.org/10.1162/tacl_a_00420  
Code: https://github.com/pzelasko/daseg

### Why I think this is important

This is one of the most directly useful papers for our classifier design because it actually fine-tunes pretrained Transformer models on **MRDA**.

More importantly, the paper does controlled experiments around **context**, which is one of the decisions we need to make ourselves. Since our current direction is local context rather than full-meeting context, this gives us an evidence-based starting point instead of choosing a context window arbitrarily.

One of the findings I especially want us to pay attention to is that context is particularly useful for distinguishing less frequent classes. That matters to us because proposal and commitment-type events are likely to be much less frequent than the dominant conversational categories.


From that, I want a practical recommendation for our **initial local-context window** rather than just a paper summary.

The point is to turn their experiments into a starting hypothesis that we can test on ICSI ourselves.

---

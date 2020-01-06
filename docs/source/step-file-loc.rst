=====================
STEP-file description
=====================

This is just an excerpt of the important parts, the full document can be viewed online at the `Library of Congress`_.
The final draft of `ISO 10303-21;2016`_ is online available at `STEP Tools, Inc.`_.

ISO 10303-21 specifies an exchange format, often known as a STEP-file, that allows product data conforming to a schema
in the EXPRESS data modeling language (ISO 10303-11) to be transferred among computer systems. The content of a
STEP-file is termed an "exchange structure." See Notes below for more on the relationship between ISO 10303-21
(STEP-file) and ISO 10303-11 (EXPRESS). This description covers the 1994-6, 2002, and 2016 versions of ISO 10303-21.

The plain text format for a STEP-file has the following characteristics:

- it consists of a sequence of records (lines of characters)
- the character set for the exchange structure is defined as the code points U+0020 to U+007E and U+0080 to U+10FFFF of
  ISO 10646 (Unicode). The first range includes: digits, upper and lower case "latin" letters, and common special
  characters (roughly equivalent to ASCII). The 2016 version of ISO 10303 extended the permitted "alphabet" to include
  "high" codepoints U+0080 to U+10FFFF, using UTF-8 encoding. For compatibility with the 2002 version, high codepoint
  characters can be encoded/escaped within "control directives" (``/X2/``, ``/X4/``, and ``/X0/``)
- the first characters in the first record are ``"ISO-10303-21;"``
- in STEP-files conforming to the 2002 version of ISO 10303-21, the last record contains ``"END-ISO-10303-21;"``
  as a terminator. A STEP-file conforming to the 2016 version may have one or more digital signatures following the
  "END-ISO-10303-21;" terminator
- text between ``"/*"`` and ``"*/"`` is a comment
- print control directives ``"\N\"`` or ``"\F\"`` can be included to indicate line-breaks or page-breaks respectively
  for use when printing the exchange structure.

The STEP-file is divided into sections. Section labels are reserved terms (termed "special tokens" in the specification)
and sections must be in the order shown below. All sections end with a record ``"ENDSEC;"``. Many STEP-file
instances have only two sections, the mandatory HEADER section and a single DATA section.

- HEADER; Mandatory, non-repeatable section.

   Must contain one instance of each of the following entities, and they shall appear in that order:

   - file_description
   - file_name
   - file_schema

   Optional entities include:

   - schema_population
   - file_population
   - section_language
   - section_context

- ANCHOR; Optional, non-repeatable section. Introduced in 2016 version. The anchor section defines external names for
  instances in the exchange structure so that they can be referenced. Anchors can be associated with entities, values,
  and other items in the exchange structure. If an anchor name is associated with an item in the REFERENCE section,
  the anchor is associated with an item in a different exchange structure.

- REFERENCE; Optional, non-repeatable section. Introduced in 2016 version. Each entry in the reference section shall
  associate an entity instance name (e.g., ``#10``) or value instance name (e.g., ``@70``) with an entity or a value,
  which may be in an external file identified by a URI. The declared references can be used in the DATA sections
  of the exchange structure.

- DATA; Optional, repeatable section. The DATA sections contain the core content of the model instance. If an exchange
  structure contains more than one DATA section, each ``"DATA"`` keyword shall be followed by a parenthesized list
  containing a name for this DATA section and a single schema name that governs the content of this section.
  Following these parameters come a sequence of entity instances, with each entity having a unique name in the form of
  ``"#"`` followed by a sequence of digits. The entities correspond to Entities and Types in the governing EXPRESS schema.
  So-called "user-defined" entities (i.e., entities not derived directly from the EXPRESS schema) are permitted but
  discouraged in the 2016 version of ISO 10303-21, which recommends (in clause 11.3) the creation of an additional
  EXPRESS schema and a separate DATA section.

- SIGNATURE; Optional, repeatable section. Introduced in 2016 version. Holds a digital signature to permit verification
  that the file content before the SIGNATURE section has not been corrupted and to validate the credentials of the
  signer. Follows the ``"END-ISO-10303-21;"`` terminator.

Also described in ISO 10303-21 is a mechanism for a multi-file exchange structure to be compressed and packaged using
ZIP. The ZIP configuration must correspond to PKZIP 2.04g, which limits compression to the Deflate algorithm. Such a
ZIP file must have a file named ``ISO10303.p21`` which serves as the "root" of the archive and contains at least the
Header of the STEP-file. The special file name ``ISO-10303.p21`` denotes the root of a multi-file exchange structure
whether stored in a ZIP archive or a directory hierarchy. This format description, apart from this paragraph, does not
cover the ZIP-based variant specified in ISO 10303-21.

.. _Library of Congress:  https://www.loc.gov/preservation/digital/formats/fdd/fdd000448.shtml

.. _ISO 10303-21;2016: http://www.steptools.com/stds/step/IS_final_p21e3.html

.. _STEP Tools, Inc.: http://www.steptools.com/
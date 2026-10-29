export type Source={id:string;title:string;url:string|null;content:string;kind:string;reliability:string};
export type Suggestion={id:string;kind:string;passage:string;replacement:string;explanation:string;requires_edit:boolean;status:string;start:number;end:number};
export type Metrics={words:number;sentences:number;average_sentence_words:number;long_sentences:number;reading_minutes:number};
export type Draft={id:string;original:string;current:string;version:number;suggestions:Suggestion[];revisions:{version:number;text:string;reason:string}[];metrics:Metrics;original_metrics:Metrics};
export type BriefItem={source_id:string;title:string;reliability:string;reliability_note:string;what_happened:{source_id:string;source_title:string;url:string|null;excerpt:string;type:string;verified:boolean}[];why_it_matters:{type:string;text:string};who_should_care:{type:string;text:string};angle:{type:string;text:string}};
export type Project={id:string;title:string;sources:Source[];brief:null|{method:string;items:BriefItem[];angle:string;limitations:string};draft:Draft|null};
export type ProjectSummary={id:string;title:string;source_count:number};

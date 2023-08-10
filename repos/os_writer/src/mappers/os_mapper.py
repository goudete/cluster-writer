TAGS = ['twitter', 'twitter_v2', 'socialmedia']


class OSMapper():
    def map(self, social_mention: dict):
        '''
        Converts Common Peakmetrics social media mention schema to legacy marty schema

        parameters:
            social_mention: dict
                deserialized common Peakmetrics social media mention schema

        returns:
            dict - data object matching the legacy marty social media mention schema
        '''
        if not social_mention:
            raise Exception('social_mention not provided')

        return {
            'Author': social_mention.get('author'),
            'created': social_mention.get('created_date'),
            'domain': social_mention.get('domain'),
            'favorite_count': social_mention.get('metadata', {}).get('favorite_count'),
            'filename': social_mention.get('text'),
            'filename_pretty': social_mention.get('text'),
            'id': social_mention.get('docs_id'),
            'language': social_mention.get('language'),
            'originalpath': social_mention.get('url'),
            'processed': social_mention.get('created_date'),
            'publish_date': social_mention.get('publish_date'),
            'retweet_count': social_mention.get('metadata', {}).get('retweet_count'),
            'sentiment_v1': {
                'polarity': social_mention.get('sentiment_v1', {}).get('polarity', 0) / 100,
                'confidence': social_mention.get('sentiment_v1', {}).get('confidence', 0) / 100,
                'label': social_mention.get('sentiment_v1', {}).get('label', ''),
            },
            'skipimageindex': True,
            'source': f'{social_mention.get("author")} - Twitter',
            'tags': TAGS,
            'text': social_mention.get('text'),
            'title': social_mention.get('text'),
            'twitter_id': social_mention.get('id'),
            'url': social_mention.get('url'),
            'user': {
                'name': social_mention.get('author'),
                'screen_name': social_mention.get('author'),
            },
            'datapipeline_v2': True,
            'workspace_id': social_mention.get('workspace_id'),
        }

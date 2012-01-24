import com.atlassian.jira.issue.IssueManager
import com.atlassian.jira.issue.CustomFieldManager
import com.atlassian.jira.user.util.UserUtil
import com.atlassian.crowd.embedded.api.User

IssueManager issueManager = componentManager.getIssueManager()
CustomFieldManager customFieldManager = componentManager.getCustomFieldManager()
UserUtil userUtil = componentManager.getUserUtil()

result = issueManager.getIssueObject('DEMO-7')
cfield = customFieldManager.getCustomFieldObjectByName('Reviewers')
result.getCustomFieldValue(cfield).each {User u ->
	u.getDisplayName()
}
